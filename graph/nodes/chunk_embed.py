"""
Chunk and Embed node: Chunks documents and creates embeddings for vector store.
"""

from typing import List, Dict
from graph.state import ReviewState


def chunk_and_embed(state: ReviewState) -> ReviewState:
    """
    Chunks documents into smaller pieces and generates embeddings.
    Stores embeddings in FAISS vector store.
    
    TODO: Implement text chunking (RecursiveCharacterTextSplitter)
    TODO: Generate embeddings using OpenAI or sentence-transformers
    TODO: Initialize FAISS index and add vectors
    TODO: Store metadata (source URL, subtopic) with each chunk
    
    Args:
        state: ReviewState with documents
        
    Returns:
        Updated ReviewState with chunks and vector_store
    """
    print(f"[CHUNK_EMBED] Processing {len(state['documents'])} documents")
    
    # TODO: from langchain.text_splitter import RecursiveCharacterTextSplitter
    # TODO: from langchain_openai import OpenAIEmbeddings
    # TODO: from langchain_community.vectorstores import FAISS
    
    # TODO: Chunk all documents
    # splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    # chunks = []
    # for doc in state["documents"]:
    #     doc_chunks = splitter.split_text(doc.content)
    #     for chunk_text in doc_chunks:
    #         chunks.append({
    #             "text": chunk_text,
    #             "metadata": {
    #                 "url": doc.url,
    #                 "title": doc.title,
    #                 "subtopic": doc.subtopic
    #             }
    #         })
    
    # TODO: Generate embeddings
    # embeddings = OpenAIEmbeddings()
    
    # TODO: Create FAISS vector store
    # texts = [chunk["text"] for chunk in chunks]
    # metadatas = [chunk["metadata"] for chunk in chunks]
    # vector_store = FAISS.from_texts(texts, embeddings, metadatas=metadatas)
    
    # Placeholder implementation
    chunks: List[Dict] = []
    for doc in state["documents"]:
        # Mock chunking
        chunks.append({
            "text": doc.content[:500],  # First 500 chars
            "metadata": {
                "url": doc.url,
                "title": doc.title,
                "subtopic": doc.subtopic
            }
        })
    
    state["chunks"] = chunks
    state["vector_store"] = None  # Placeholder, will be FAISS instance
    
    return state
