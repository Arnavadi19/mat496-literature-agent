"""
Planner node: Generates subtopics and search queries using structured output.
"""

import os
from pathlib import Path
from typing import List
from graph.state import ReviewState, Subtopic
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


class SubtopicsPlan(BaseModel):
    """Structured output for the planner."""
    subtopics: List[Subtopic] = Field(
        description="List of 3-6 research subtopics with search queries"
    )


def plan_subtopics(state: ReviewState) -> ReviewState:
    """
    Analyzes the research topic and generates 3-6 subtopics with search queries.
    
    Uses OpenAI's structured output to ensure Pydantic model compliance.
    
    Args:
        state: Current ReviewState
        
    Returns:
        Updated ReviewState with subtopics populated
    """
    print(f"[PLANNER] Planning subtopics for: {state['topic']}")
    
    # Load prompt template
    prompt_path = Path(__file__).parent.parent.parent / "prompts" / "planner_prompt.txt"
    with open(prompt_path, 'r') as f:
        prompt_template = f.read()
    
    # Format prompt with topic
    prompt = prompt_template.format(topic=state['topic'])
    
    try:
        # Initialize OpenAI with structured output
        llm = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4"),
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Use structured output (with_structured_output)
        structured_llm = llm.with_structured_output(SubtopicsPlan, method="function_calling")
        
        # Invoke LLM
        print("  Calling OpenAI for subtopic planning...")
        result = structured_llm.invoke(prompt)
        
        # Extract subtopics
        state["subtopics"] = result.subtopics
        print(f"  Generated {len(result.subtopics)} subtopics")
        
    except Exception as e:
        print(f"  ⚠️  Error calling OpenAI: {e}")
        print("  Using fallback placeholder subtopics")
        
        # Fallback to placeholder subtopics
        state["subtopics"] = [
            Subtopic(
                name="Foundational Overview",
                search_query=f"{state['topic']} overview introduction",
                rationale="Provides foundational understanding"
            ),
            Subtopic(
                name="Recent Advances",
                search_query=f"{state['topic']} recent developments 2024",
                rationale="Covers latest developments"
            ),
            Subtopic(
                name="Challenges and Limitations",
                search_query=f"{state['topic']} challenges limitations",
                rationale="Identifies open problems"
            ),
        ]
    
    return state
