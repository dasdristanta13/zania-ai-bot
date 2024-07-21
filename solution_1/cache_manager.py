"""
cache_manager.py: Manages caching functionality for the QA Bot
"""

import sqlite3
import json
import hashlib
from typing import Dict, Optional

class CacheManager:
    """
    A class to manage caching of question-answer pairs in a SQLite database.
    """

    def __init__(self, db_path: str):
        """
        Initialize the CacheManager with the path to the SQLite database.

        Args:
            db_path (str): The file path to the SQLite database.
        """
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """
        Initialize the SQLite database by creating the qa_cache table if it doesn't exist.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Create the qa_cache table if it doesn't exist
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS qa_cache (
                question_hash TEXT PRIMARY KEY,
                question TEXT,
                answer TEXT,
                sources TEXT
            )
            ''')
            conn.commit()

    def get_cached_answer(self, question: str) -> Optional[Dict[str, str]]:
        """
        Retrieve a cached answer from the database for a given question.

        Args:
            question (str): The question to look up in the cache.

        Returns:
            Optional[Dict[str, str]]: A dictionary containing the answer and sources if found, None otherwise.
        """
        question_hash = self._compute_question_hash(question)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Query the database for the cached answer
            cursor.execute("SELECT answer, sources FROM qa_cache WHERE question_hash = ?", (question_hash,))
            result = cursor.fetchone()

        if result:
            return {"answer": result[0], "sources": json.loads(result[1])}
        return None

    def cache_answer(self, question: str, answer: str, sources: list):
        """
        Cache an answer in the database for a given question.

        Args:
            question (str): The question to cache.
            answer (str): The answer to cache.
            sources (list): The sources associated with the answer.
        """
        question_hash = self._compute_question_hash(question)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Insert or replace the answer in the cache
            cursor.execute(
                "INSERT OR REPLACE INTO qa_cache (question_hash, question, answer, sources) VALUES (?, ?, ?, ?)",
                (question_hash, question, answer, json.dumps(sources))
            )
            conn.commit()

    @staticmethod
    def _compute_question_hash(question: str) -> str:
        """
        Compute a hash of the question to use as a cache key.

        Args:
            question (str): The question to hash.

        Returns:
            str: The MD5 hash of the lowercase question.
        """
        # Convert question to lowercase and compute MD5 hash
        return hashlib.md5(question.lower().encode()).hexdigest()