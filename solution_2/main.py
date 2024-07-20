import os
import json
import logging
from pathlib import Path
from dotenv import load_dotenv

from pdf_extractor import PDFExtractor
from chain import ChainManager
from slack_post import SlackManager
from cache_manager import CacheManager

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
env_path = Path('env\.env') 
load_dotenv(dotenv_path=env_path)

# Initialize API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# SQLite database setup
DB_PATH = 'qa_cache.db'

def process_questions(qa_chain, questions, cache_manager):
    """Process a list of questions and return results."""
    results = {}
    for question in questions:
        try:
            # Check if the question is in the cache
            cached_result = cache_manager.get_cached_answer(question)
            if cached_result:
                logger.info(f"Cache hit for question: {question}")
                results[question] = cached_result
            else:
                logger.info(f"Cache miss for question: {question}")
                answer, sources = ChainManager.process_query(qa_chain, question)
                result = {
                    "answer": answer,
                    "sources": [f"Section {doc.metadata.get('section', 'N/A')}, Page {doc.metadata.get('page', 'N/A')}" for doc in sources[:10]]
                }
                results[question] = result
                
                # Update the cache
                cache_manager.cache_answer(question, answer, result["sources"])
        except Exception as e:
            logger.error(f"Error processing question '{question}': {e}")
            results[question] = {"answer": "An error occurred while processing this question.", "sources": []}
    
    return results

def main(pdf_path, questions):
    """Main function to process PDF and answer questions."""
    try:
        # Initialize managers
        cache_manager = CacheManager(DB_PATH)
        pdf_extractor = PDFExtractor()
        chain_manager = ChainManager(OPENAI_API_KEY)
        slack_manager = SlackManager(SLACK_BOT_TOKEN)

        # Process PDF
        pages = pdf_extractor.get_pdf_text(pdf_path)
        if not pages:
            raise ValueError("Failed to extract text from PDF")

        text_chunks = pdf_extractor.get_text_chunks(pages)
        if not text_chunks:
            raise ValueError("Failed to create text chunks")

        vectorstore = pdf_extractor.get_vectorstore(text_chunks, pdf_path)
        if not vectorstore:
            raise ValueError("Failed to create vector store")

        qa_chain = chain_manager.create_advanced_chain(vectorstore)
        if not qa_chain:
            raise ValueError("Failed to create QA chain")

        # Process questions and get answers
        results = process_questions(qa_chain, questions, cache_manager)

        # Convert results to JSON
        json_results = json.dumps(results, indent=2)

        # Post results to Slack
        slack_channel = "#qa"
        slack_manager.post_to_slack(slack_channel, f"AI Agent Results:\n```{json_results}```")

        return json_results
    except Exception as e:
        logger.error(f"An error occurred in the main function: {e}")
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    pdf_path = "data/handbook.pdf"
    questions = [
        "What is the name of the company?",
        "Who is the CEO of the company?",
        "What is their vacation policy?",
        "What is the termination policy?"
    ]
    results = main(pdf_path, questions)
    print(results)