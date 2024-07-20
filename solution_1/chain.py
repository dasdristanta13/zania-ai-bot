"""
chain.py: Manages the creation and usage of the QA chain
"""

from langchain.chat_models import ChatOpenAI
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.prompts import PromptTemplate

class ChainManager:
    def __init__(self, openai_api_key):
        self.openai_api_key = openai_api_key

    def create_advanced_chain(self, vectorstore):
        llm = ChatOpenAI(model_name="gpt-3.5-turbo-0125", temperature=0.00001, openai_api_key=self.openai_api_key)
        
        base_retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k":5})
        compressor = LLMChainExtractor.from_llm(llm)
        compression_retriever = ContextualCompressionRetriever(
            base_compressor=compressor,
            base_retriever=base_retriever
        )
        
        context_prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="Given the following context:\n\n{context}\n\nAnswer the following question: {question}\n\nIf the answer is not explicitly stated in the context, try to find keywords matching. Else, say 'Data Not Available'."
        )
        
        document_prompt = PromptTemplate(
            input_variables=["page_content"],
            template="{page_content}"
        )
        
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
        response = chain({"query": query})
        return response['result'], response['source_documents']