"""
chain.py: Manages the creation and execution of the question-answering chain.

This module sets up an advanced retrieval-based question-answering system
using LangChain components. It combines dense and sparse retrievers,
applies contextual compression, and uses a custom prompt for answering questions.
"""
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.retrievers import EnsembleRetriever
import logging
from langchain_community.chat_models import ChatOpenAI
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ChainManager:
    def __init__(self, openai_api_key):
        """
        Initialize the ChainManager with the OpenAI API key.

        Args:
        openai_api_key (str): The OpenAI API key for authentication
        """
        self.openai_api_key = openai_api_key

    def create_advanced_chain(self, vectorstore):
        """
        Create an advanced question-answering chain.

        This method sets up a complex retrieval system combining dense and sparse
        retrievers, applies contextual compression, and uses custom prompts.

        Args:
        vectorstore: The vector store containing the document embeddings

        Returns:
        RetrievalQA: The question-answering chain, or None if an error occurs
        """
        try:
            # Initialize the language model
            llm = ChatOpenAI(model_name="gpt-3.5-turbo-0125", temperature=0.00001, openai_api_key=self.openai_api_key)
            
            # Create dense retriever
            dense_retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 5})
            
            # Create sparse retriever (BM25)
            documents = self.prepare_documents(vectorstore.get())
            bm25_retriever = BM25Retriever.from_documents(documents)
            bm25_retriever.k = 5
            
            # Create ensemble retriever
            ensemble_retriever = EnsembleRetriever(
                retrievers=[dense_retriever, bm25_retriever],
                weights=[0.5, 0.5]
            )
            
            # Apply contextual compression
            compressor = LLMChainExtractor.from_llm(llm)
            compression_retriever = ContextualCompressionRetriever(
                base_compressor=compressor,
                base_retriever=ensemble_retriever
            )
            
            # Define custom prompts
            context_prompt = PromptTemplate(
                input_variables=["context", "question"],
                template="Given the following context:\n\n{context}\n\nAnswer the following question: {question}\n\nIf the answer is not explicitly stated in the context, try to find keywords matching. Else, say 'Data Not Available'. Include the section number in your response when possible."
            )
            
            document_prompt = PromptTemplate(
                input_variables=["page_content", "section"],
                template="[Section {section}] {page_content}"
            )
            
            # Create the QA chain
            qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=compression_retriever,
                return_source_documents=True,
                chain_type_kwargs={
                    "prompt": context_prompt,
                    "document_prompt": document_prompt,
                }
            )
            
            return qa_chain
        except Exception as e:
            logger.error(f"Error creating advanced chain: {e}")
            return None

    @staticmethod
    def prepare_documents(docs):
        """
        Prepare documents for use in the BM25 retriever.

        Args:
        docs: The documents to prepare

        Returns:
        list: A list of prepared Document objects
        """
        prepared_docs = []
        for doc in docs:
            if isinstance(doc, Document):
                prepared_docs.append(doc)
            elif isinstance(doc, str):
                prepared_docs.append(Document(page_content=doc, metadata={}))
            else:
                logger.warning(f"Unexpected document type: {type(doc)}. Skipping.")
        return prepared_docs

    @staticmethod
    def process_query(chain, query):
        """
        Process a query using the QA chain.

        Args:
        chain: The question-answering chain
        query (str): The question to process

        Returns:
        tuple: A tuple containing the answer and source documents
        """
        try:
            response = chain({"query": query})
            return response['result'], response['source_documents']
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return "An error occurred while processing the query.", []