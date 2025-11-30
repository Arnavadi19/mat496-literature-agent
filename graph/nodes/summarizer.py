"""
Summarizer node: Creates academic summaries for each subtopic.
"""

import os
from pathlib import Path
from typing import List
from graph.state import ReviewState, Summary
from langchain_openai import ChatOpenAI


def summarize_subtopics(state: ReviewState) -> ReviewState:
    """
    For each subtopic, uses LLM to summarize retrieved chunks into
    clean academic summaries.
    
    Args:
        state: ReviewState with retrieved chunks
        
    Returns:
        Updated ReviewState with summaries
    """
    print(f"[SUMMARIZER] Summarizing {len(state['subtopics'])} subtopics")
    
    # Load prompt template
    prompt_path = Path(__file__).parent.parent.parent / "prompts" / "summarizer_prompt.txt"
    with open(prompt_path, 'r') as f:
        prompt_template = f.read()
    
    retrieved_chunks = state.get("_retrieved_chunks", {})
    summaries: List[Summary] = []
    
    # Initialize LLM
    try:
        llm = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4"),
            temperature=0.3,  # Lower temperature for more focused summaries
            api_key=os.getenv("OPENAI_API_KEY")
        )
        structured_llm = llm.with_structured_output(Summary)
    except Exception as e:
        print(f"  ⚠️  Error initializing OpenAI: {e}")
        llm = None
    
    for subtopic in state["subtopics"]:
        chunks = retrieved_chunks.get(subtopic.name, [])
        print(f"  Summarizing: {subtopic.name} ({len(chunks)} chunks)")
        
        # Format documents for prompt
        documents_text = "\n\n".join([
            f"Document {i+1} ({chunk['metadata']['url']}):\n{chunk['text']}"
            for i, chunk in enumerate(chunks[:10])  # Limit to top 10 chunks
        ])
        
        # Format prompt
        prompt = prompt_template.format(
            subtopic=subtopic.name,
            query=subtopic.search_query,
            documents=documents_text if documents_text else "No documents retrieved."
        )
        
        if llm:
            try:
                # Call LLM with structured output
                summary = structured_llm.invoke(prompt)
                summaries.append(summary)
                print(f"    ✓ Generated summary with {len(summary.key_findings)} findings")
                
            except Exception as e:
                print(f"    ⚠️  Error generating summary: {e}. Using placeholder.")
                summaries.append(_create_placeholder_summary(subtopic.name, chunks))
        else:
            summaries.append(_create_placeholder_summary(subtopic.name, chunks))
    
    state["summaries"] = summaries
    return state


def _create_placeholder_summary(subtopic_name: str, chunks: List) -> Summary:
    """Creates a placeholder summary when LLM call fails."""
    return Summary(
        subtopic=subtopic_name,
        summary=f"Academic summary for {subtopic_name}. "
                f"Based on {len(chunks)} retrieved sources.",
        key_findings=[
            "Finding 1: Placeholder finding (OpenAI integration needed)",
            "Finding 2: Another placeholder finding",
        ],
        sources=[chunk["metadata"]["url"] for chunk in chunks[:3]] if chunks else []
    )
