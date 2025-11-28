"""
Planner node: Generates subtopics and search queries using structured output.
"""

from typing import List
from graph.state import ReviewState, Subtopic
from langchain_openai import ChatOpenAI
from pydantic import BaseModel


# TODO: Set your OpenAI API key in environment variables
# export OPENAI_API_KEY='your-key-here'


class SubtopicsPlan(BaseModel):
    """Structured output for the planner."""
    subtopics: List[Subtopic]


def plan_subtopics(state: ReviewState) -> ReviewState:
    """
    Analyzes the research topic and generates 3-6 subtopics with search queries.
    
    Uses OpenAI's structured output to ensure Pydantic model compliance.
    
    Args:
        state: Current ReviewState
        
    Returns:
        Updated ReviewState with subtopics populated
    """
    # TODO: Load prompt from prompts/planner_prompt.txt
    # TODO: Implement OpenAI structured output API call
    # TODO: Parse response into Subtopic objects
    
    print(f"[PLANNER] Planning subtopics for: {state['topic']}")
    
    # Placeholder implementation
    # Replace this with actual LLM call using structured output
    placeholder_subtopics = [
        Subtopic(
            name="Subtopic 1",
            search_query=f"{state['topic']} overview",
            rationale="Provides foundational understanding"
        ),
        Subtopic(
            name="Subtopic 2",
            search_query=f"{state['topic']} recent advances",
            rationale="Covers latest developments"
        ),
        Subtopic(
            name="Subtopic 3",
            search_query=f"{state['topic']} challenges",
            rationale="Identifies open problems"
        ),
    ]
    
    state["subtopics"] = placeholder_subtopics
    return state
