"""
State definition for the Literature Review Agent.

This module defines the ReviewState TypedDict that flows through the LangGraph.
"""

from typing import TypedDict, List, Dict, Optional
from pydantic import BaseModel


class Subtopic(BaseModel):
    """Structured representation of a research subtopic."""
    name: str
    search_query: str
    rationale: str


class Document(BaseModel):
    """Represents a fetched document."""
    url: str
    title: str
    content: str
    subtopic: str


class Summary(BaseModel):
    """Academic summary for a subtopic."""
    subtopic: str
    summary: str
    key_findings: List[str]
    sources: List[str]


class ReviewState(TypedDict):
    """
    State object that flows through the LangGraph.
    
    Fields:
        topic: The main research topic provided by the user
        subtopics: List of generated subtopics with queries
        documents: Raw documents fetched from web
        chunks: Chunked and embedded document fragments
        summaries: Per-subtopic academic summaries
        final_review: Complete synthesized literature review
        vector_store: FAISS vector store instance (optional)
    """
    topic: str
    subtopics: List[Subtopic]
    documents: List[Document]
    chunks: List[Dict[str, any]]  # Will contain text, embeddings, metadata
    summaries: List[Summary]
    final_review: Optional[str]
    vector_store: Optional[any]  # FAISS vector store
