"""
pdf_extractor.py: Manages PDF extraction and vectorization
"""

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import os

class PDFExtractor:
    PERSIST_DIRECTORY = 'db'

    def __init__(self):
        self.openai_ef = OpenAIEmbeddings(model="text-embedding-ada-002")

    @staticmethod
    def get_pdf_text(pdf_path):
        loader = PyPDFLoader(pdf_path)
        pages = loader.load_and_split()
        return pages

    @staticmethod
    def get_text_chunks(pages):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=400,
            length_function=len
        )
        chunks = []
        for page in pages:
            page_chunks = text_splitter.split_text(page.page_content)
            for chunk in page_chunks:
                chunks.append(Document(page_content=chunk, metadata={"page": page.metadata["page"]}))
        return chunks

    def get_vectorstore(self, text_chunks, pdf_path):
        pdf_id = os.path.basename(pdf_path).replace('.pdf', '')
        persist_directory = os.path.join(self.PERSIST_DIRECTORY, pdf_id)
        
        if os.path.exists(persist_directory):
            print("Loading existing vector store...")
            return Chroma(persist_directory=persist_directory, embedding_function=self.openai_ef)
        
        print("Creating new vector store...")
        vectorstore = Chroma.from_documents(
            documents=text_chunks,
            embedding=self.openai_ef,
            persist_directory=persist_directory
        )
        vectorstore.persist()
        return vectorstore