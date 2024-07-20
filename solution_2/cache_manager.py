import sqlite3
import json
import hashlib
from typing import Dict, Any, List, Union

class CacheManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """Initialize the SQLite database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS qa_cache (
                question_hash TEXT PRIMARY KEY,
                question TEXT,
                answer TEXT,
                sources TEXT
            )
            ''')
            conn.commit()

    def get_cached_answer(self, question: str) -> Union[Dict[str, Union[str, List[str]]], None]:
        """Retrieve a cached answer from the database."""
        question_hash = self._compute_question_hash(question)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT answer, sources FROM qa_cache WHERE question_hash = ?", (question_hash,))
            result = cursor.fetchone()

        if result:
            return {"answer": result[0], "sources": json.loads(result[1])}
        return None

    def cache_answer(self, question: str, answer: str, sources: Any):
        """Cache an answer in the database."""
        question_hash = self._compute_question_hash(question)
        
        # Convert sources to a JSON-serializable format
        if isinstance(sources, dict):
            serializable_sources = list(sources.keys())  # Convert dict_keys to list
        elif isinstance(sources, (list, tuple)):
            serializable_sources = list(sources)
        else:
            serializable_sources = [str(sources)]  # Wrap single items in a list
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO qa_cache (question_hash, question, answer, sources) VALUES (?, ?, ?, ?)",
                (question_hash, question, answer, json.dumps(serializable_sources))
            )
            conn.commit()

    @staticmethod
    def _compute_question_hash(question: str) -> str:
        """Compute a hash of the question to use as a cache key."""
        return hashlib.md5(question.lower().encode()).hexdigest()