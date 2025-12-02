"""
Chunk and Embed node: Chunks documents and creates embeddings for vector store.
"""

import os
from typing import List, Dict
from graph.state import ReviewState
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


def chunk_and_embed(state: ReviewState) -> ReviewState:
    """
    Chunks documents into smaller pieces and generates embeddings.
    Stores embeddings in FAISS vector store.
    
    Implements complete RAG pipeline:
    1. Splits documents into chunks with overlap
    2. Generates embeddings using OpenAI
    3. Creates FAISS index for semantic search
    4. Stores metadata with each chunk
    
    Args:
        state: ReviewState with documents
        
    Returns:
        Updated ReviewState with chunks and vector_store
    """
    print(f"[CHUNK_EMBED] Processing {len(state['documents'])} documents")
    
    if not state["documents"]:
        print("  Warning: No documents to process")
        state["chunks"] = []
        state["vector_store"] = None
        return state
    
    try:
        # Initialize text splitter
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        print("  Chunking documents...")
        chunks = []
        texts = []
        metadatas = []
        
        # Chunk all documents
        for doc in state["documents"]:
            doc_chunks = splitter.split_text(doc.content)
            
            for chunk_text in doc_chunks:
                chunks.append({
                    "text": chunk_text,
                    "metadata": {
                        "url": doc.url,
                        "title": doc.title,
                        "subtopic": doc.subtopic
                    }
                })
                texts.append(chunk_text)
                metadatas.append({
                    "url": doc.url,
                    "title": doc.title,
                    "subtopic": doc.subtopic
                })
        
        print(f"  Created {len(chunks)} chunks from {len(state['documents'])} documents")
        
        # Generate embeddings and create FAISS vector store
        print("  Generating embeddings and creating FAISS index...")
        
        embeddings = OpenAIEmbeddings(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Create FAISS vector store
        vector_store = FAISS.from_texts(
            texts=texts,
            embedding=embeddings,
            metadatas=metadatas
        )
        
        print(f"  FAISS index created with {len(texts)} vectors")
        
        state["chunks"] = chunks
        state["vector_store"] = vector_store
        
    except Exception as e:
        print(f"  Warning: Error in chunking/embedding: {e}")
        print("  Using placeholder chunks without embeddings")
        
        # Fallback: Create simple chunks without embeddings
        chunks = []
        for doc in state["documents"]:
            chunks.append({
                "text": doc.content[:1000],  # First 1000 chars
                "metadata": {
                    "url": doc.url,
                    "title": doc.title,
                    "subtopic": doc.subtopic
                }
            })
        
        state["chunks"] = chunks
        state["vector_store"] = None
    
    return state
