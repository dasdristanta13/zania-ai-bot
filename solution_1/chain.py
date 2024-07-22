"""
chain.py: Manages the creation and usage of the QA chain
"""
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import PromptTemplate

class ChainManager:
    """
    A class to manage the creation and usage of a question-answering chain.
    """

    def __init__(self, openai_api_key):
        """
        Initialize the ChainManager with the OpenAI API key.

        Args:
            openai_api_key (str): The API key for OpenAI.
        """
        self.openai_api_key = openai_api_key

    def create_advanced_chain(self, vectorstore):
        """
        Create an advanced QA chain using the provided vectorstore.

        Args:
            vectorstore: The vectorstore to use for document retrieval.

        Returns:
            RetrievalQA: An advanced QA chain ready for querying.
        """
        # Create a ChatOpenAI instance with specific parameters
        llm = ChatOpenAI(model_name="gpt-3.5-turbo-0125", temperature=0.00001, openai_api_key=self.openai_api_key)
        
        # Set up the base retriever using the vectorstore
        base_retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k":5})
        
        # Create a compressor using the LLM
        compressor = LLMChainExtractor.from_llm(llm)
        
        # Set up a contextual compression retriever
        compression_retriever = ContextualCompressionRetriever(
            base_compressor=compressor,
            base_retriever=base_retriever
        )
        
        # Define the context prompt template
        context_prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="Given the following context:\n\n{context}\n\nAnswer the following question: {question}\n\nIf the answer is not explicitly stated in the context, try to find keywords matching. Else, say 'Data Not Available'."
        )
        
        # Define the document prompt template
        document_prompt = PromptTemplate(
            input_variables=["page_content"],
            template="{page_content}"
        )
        
        # Create the QA chain using RetrievalQA
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

    @staticmethod
    def process_query(chain, query):
        """
        Process a query using the provided QA chain.

        Args:
            chain (RetrievalQA): The QA chain to use for processing the query.
            query (str): The query to process.

        Returns:
            tuple: A tuple containing the result and source documents.
        """
        # Process a query using the QA chain and return the result and source documents
        response = chain({"query": query})
        return response['result'], response['source_documents']