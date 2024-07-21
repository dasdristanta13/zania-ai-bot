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
    """
    A class to handle PDF extraction and vectorization for document processing.
    """

    PERSIST_DIRECTORY = 'db'

    def __init__(self):
        """
        Initialize the PDFExtractor with OpenAI embeddings.
        """
        # Initialize OpenAI embeddings model
        self.openai_ef = OpenAIEmbeddings(model="text-embedding-ada-002")

    @staticmethod
    def get_pdf_text(pdf_path: str) -> list:
        """
        Extract text from a PDF file.

        Args:
            pdf_path (str): The file path to the PDF.

        Returns:
            list: A list of page contents from the PDF.
        """
        # Load and split the PDF into pages
        loader = PyPDFLoader(pdf_path)
        pages = loader.load_and_split()
        return pages

    @staticmethod
    def get_text_chunks(pages: list) -> list:
        """
        Split the text from PDF pages into smaller chunks.

        Args:
            pages (list): A list of page contents from a PDF.

        Returns:
            list: A list of Document objects, each containing a chunk of text.
        """
        # Initialize the text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=400,
            length_function=len
        )
        chunks = []
        # Split each page into chunks
        for page in pages:
            page_chunks = text_splitter.split_text(page.page_content)
            for chunk in page_chunks:
                chunks.append(Document(page_content=chunk, metadata={"page": page.metadata["page"]}))
        return chunks

    def get_vectorstore(self, text_chunks: list, pdf_path: str) -> Chroma:
        """
        Create or load a vector store for the given text chunks.

        Args:
            text_chunks (list): A list of text chunks to vectorize.
            pdf_path (str): The file path to the original PDF.

        Returns:
            Chroma: A Chroma vector store containing the vectorized text chunks.
        """
        # Generate a unique ID for the PDF
        pdf_id = os.path.basename(pdf_path).replace('.pdf', '')
        persist_directory = os.path.join(self.PERSIST_DIRECTORY, pdf_id)
        
        # Check if a vector store already exists for this PDF
        if os.path.exists(persist_directory):
            print("Loading existing vector store...")
            return Chroma(persist_directory=persist_directory, embedding_function=self.openai_ef)
        
        # Create a new vector store if one doesn't exist
        print("Creating new vector store...")
        vectorstore = Chroma.from_documents(
            documents=text_chunks,
            embedding=self.openai_ef,
            persist_directory=persist_directory
        )
        vectorstore.persist()
        return vectorstore