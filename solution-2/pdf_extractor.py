from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import os
import re
import logging
from typing import List, Union

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PDFExtractor:
    PERSIST_DIRECTORY = 'db'

    def __init__(self):
        self.openai_ef = OpenAIEmbeddings(model="text-embedding-ada-002")

    @staticmethod
    def get_pdf_text(pdf_path: str) -> List[Document]:
        try:
            loader = PyPDFLoader(pdf_path)
            pages = loader.load_and_split()
            return pages
        except Exception as e:
            logger.error(f"Error loading PDF: {e}")
            return []

    @staticmethod
    def get_text_chunks(pages: List[Document]) -> List[Document]:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=400,
            length_function=len
        )
        chunks = []
        for page in pages:
            try:
                page_chunks = text_splitter.split_text(page.page_content)
                for chunk in page_chunks:
                    section = PDFExtractor.extract_section(chunk)
                    chunks.append(Document(page_content=chunk, metadata={"page": page.metadata.get("page", "N/A"), "section": section}))
            except Exception as e:
                logger.error(f"Error processing page: {e}")
        return chunks

    @staticmethod
    def extract_section(text: str) -> str:
        try:
            section_match = re.search(r'\b(\d+\.\d+)\b', text)
            if section_match:
                return section_match.group(1)
        except Exception as e:
            logger.error(f"Error extracting section: {e}")
        return "N/A"

    def get_vectorstore(self, text_chunks: List[Document], pdf_path: str) -> Chroma:
        pdf_id = os.path.basename(pdf_path).replace('.pdf', '')
        persist_directory = os.path.join(self.PERSIST_DIRECTORY, pdf_id)
        
        if os.path.exists(persist_directory):
            logger.info("Loading existing vector store...")
            return Chroma(persist_directory=persist_directory, embedding_function=self.openai_ef)
        
        logger.info("Creating new vector store...")
        unique_chunks = PDFExtractor.remove_duplicates(text_chunks)
        try:
            vectorstore = Chroma.from_documents(
                documents=unique_chunks,
                embedding=self.openai_ef,
                persist_directory=persist_directory
            )
            vectorstore.persist()
            return vectorstore
        except Exception as e:
            logger.error(f"Error creating vector store: {e}")
            return None

    @staticmethod
    def remove_duplicates(chunks: List[Union[Document, str]]) -> List[Document]:
        seen = set()
        unique_chunks = []
        for chunk in chunks:
            try:
                if isinstance(chunk, Document):
                    content = chunk.page_content
                elif isinstance(chunk, str):
                    content = chunk
                else:
                    logger.warning(f"Unexpected chunk type: {type(chunk)}. Skipping.")
                    continue

                if content not in seen:
                    seen.add(content)
                    if isinstance(chunk, str):
                        chunk = Document(page_content=chunk, metadata={})
                    unique_chunks.append(chunk)
            except Exception as e:
                logger.error(f"Error processing chunk: {e}")
        return unique_chunks