"""Vector store using TF-IDF for similarity search (no API key needed for embeddings)."""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class LocalVectorStore:
    """Simple TF-IDF based vector store — no external API needed."""

    def __init__(self, texts: list[str]):
        self.texts = texts
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.tfidf_matrix = self.vectorizer.fit_transform(texts)

    def similarity_search(self, query: str, k: int = 4) -> list[str]:
        """Find the k most similar chunks to the query."""
        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        top_indices = similarities.argsort()[-k:][::-1]
        return [self.texts[i] for i in top_indices]


def create_vector_store(text_chunks: list[str]):
    """Create a local TF-IDF vector store from text chunks."""
    return LocalVectorStore(text_chunks)


def similarity_search(vector_store, query: str, k: int = 4) -> list[str]:
    """Retrieve the most relevant chunks for a query."""
    return vector_store.similarity_search(query, k=k)
