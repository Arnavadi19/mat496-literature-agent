# Autonomous Literature Review Agent

A modern AI-powered literature review assistant built with **LangGraph**, **LangChain**, and **OpenAI**, demonstrating cutting-edge agentic AI concepts including RAG, tool calling, and structured outputs.

## Overview

This project implements an autonomous AI agent that generates comprehensive academic literature reviews on any research topic. The agent uses LangGraph to orchestrate a multi-stage workflow: planning subtopics with GPT-4, searching the web with DuckDuckGo, fetching and processing documents, building a FAISS vector store for semantic search, and synthesizing a complete literature review. The system demonstrates agent architectures including conditional edges for quality checks, retry logic, and intelligent caching.

## Motivation

This project aligns with course objectives by implementing a practical agentic system using state-of-the-art techniques in natural language processing and information retrieval. It demonstrates key concepts including LangGraph workflows, Retrieval-Augmented Generation (RAG) pipelines, vector embeddings, semantic search with FAISS, and structured LLM outputs. The agent architecture showcases how multiple AI components can work together autonomously to solve complex research tasks.

As a researcher in computer vision, I spend considerable time browsing the internet for papers and articles on novel techniques. Since the inception of agentic AI, I wanted a search tool (similar to ChatGPT Deep Research) that would conduct preliminary research automatically, saving time and streamlining the literature review process. This project addresses that need by automating the tedious task of gathering, synthesizing, and organizing research materials.

## Project Overview

This agent autonomously conducts comprehensive literature reviews by:
1. **Planning** subtopics using structured LLM outputs
2. **Searching** the web for relevant academic sources
3. **Fetching** and processing webpage content
4. **Embedding** documents into a vector store (FAISS)
5. **Retrieving** semantically relevant chunks per subtopic
6. **Summarizing** findings with LLM-powered synthesis
7. **Synthesizing** a complete academic literature review

## Architecture

### LangGraph Workflow

```mermaid
graph LR
    A[Start] --> B[Plan Subtopics]
    B --> C[Search Web]
    C --> D[Fetch Pages]
    D --> E[Chunk & Embed]
    E --> F[Retrieve Context]
    F --> G[Summarize Subtopics]
    G --> H[Synthesize Review]
    H --> I[End]
```

### Key Concepts Demonstrated

- **State Management**: TypedDict-based state flows through the graph
- **Node Functions**: Pure functions that transform state
- **Structured Output**: Pydantic models for LLM responses
- **RAG Pipeline**: Semantic search with FAISS + embeddings
- **Tool Calling**: LLM-powered tools for search and retrieval
- **Modular Prompts**: Templated prompts for consistency

## Project Structure

```
project/
├── main.py                      # Entry point & graph construction
├── graph/
│   ├── __init__.py
│   ├── state.py                 # ReviewState TypedDict & Pydantic models
│   └── nodes/                   # LangGraph node implementations
│       ├── planner.py           # Subtopic planning with structured output
│       ├── searcher.py          # Web search orchestration
│       ├── fetcher.py           # Content fetching
│       ├── chunk_embed.py       # Document chunking & embedding
│       ├── retriever.py         # Semantic search
│       ├── summarizer.py        # Per-subtopic summarization
│       └── synthesizer.py       # Final review synthesis
├── tools/
│   ├── search_tool.py           # Brave/SerpAPI integration
│   └── fetch_tool.py            # Web scraping utilities
├── prompts/
│   ├── planner_prompt.txt       # Planning prompt template
│   ├── summarizer_prompt.txt    # Summarization template
│   └── synthesizer_prompt.txt   # Synthesis template
├── vectorstore/
│   └── __init__.py              # FAISS utilities (TODO)
├── requirements.txt
└── README.md
```

## Quick Start

### 1. Installation

```bash
# Clone or navigate to project directory
cd mat496-project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Set your API keys:

```bash
export OPENAI_API_KEY='your-openai-key-here'

# Optional: For web search
export BRAVE_API_KEY='your-brave-key'
# OR
export SERPAPI_KEY='your-serpapi-key'
```

### 3. Run

```bash
python main.py
```

## Implementation Roadmap

### Phase 1: Core LLM Integration  **COMPLETED**

**Status**: All core LLM integration nodes implemented

**Completed Tasks**:
- [x] **Planner Node** (`graph/nodes/planner.py`)
  - [x] Load prompt from `prompts/planner_prompt.txt`
  - [x] Implement OpenAI structured output API call
  - [x] Use `SubtopicsPlan` Pydantic model for response parsing
  - [x] Handle API errors with fallback to placeholder subtopics

- [x] **Summarizer Node** (`graph/nodes/summarizer.py`)
  - [x] Load prompt template
  - [x] Format retrieved chunks into prompt
  - [x] Call OpenAI with structured output (`Summary` model)
  - [x] Error handling with placeholder summaries

- [x] **Synthesizer Node** (`graph/nodes/synthesizer.py`)
  - [x] Load synthesis prompt
  - [x] Aggregate all subtopic summaries
  - [x] Generate comprehensive review via LLM
  - [x] Fallback to structured placeholder on errors

**Resources**:
- [OpenAI Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs)
- [LangChain ChatOpenAI docs](https://python.langchain.com/docs/integrations/chat/openai)

---

### Phase 2: Search & Fetch Integration **COMPLETED**

**Status**: Free DuckDuckGo search integrated (no API key required)

**Completed Tasks**:
- [x] **Search Tool** (`tools/search_tool.py`)
  - [x] Implemented DuckDuckGo search (free, no API key needed)
  - [x] Added SerpAPI support as optional paid alternative
  - [x] Error handling with automatic fallback
  - [x] Return structured results (title, URL, snippet)

- [x] **Searcher Node** (`graph/nodes/searcher.py`)
  - [x] Integrated DuckDuckGo search
  - [x] Query each subtopic's search_query
  - [x] Store URLs in state
  - [x] Graceful error handling

**Remaining Tasks**:
- [ ] **Fetch Tool** (`tools/fetch_tool.py`) - partially implemented
  - [ ] Consider using `trafilatura` for better text extraction
  - [ ] Implement concurrent fetching with `ThreadPoolExecutor`
  - [ ] Add robust error handling (timeouts, 404s, etc.)

- [ ] **Fetcher Node** (`graph/nodes/fetcher.py`) - uses placeholder
  - [ ] Integrate real URL fetching
  - [ ] Create `Document` objects with actual content
  - [ ] Handle fetch failures gracefully

---

### Phase 3: RAG Pipeline (Vector Store + Retrieval) **NEXT**

**Tasks**:
- [ ] **Search Tool** (`tools/search_tool.py`)
  - [ ] Choose search backend (Brave recommended for API simplicity)
  - [ ] Install SDK: `pip install brave-search-python` or `google-search-results`
  - [ ] Implement `search_brave()` with error handling
  - [ ] Add rate limiting (respect API quotas)
  - [ ] Return structured results (title, URL, snippet)

- [ ] **Fetch Tool** (`tools/fetch_tool.py`)
  - [ ] Consider using `trafilatura` for better text extraction
  - [ ] Implement concurrent fetching with `ThreadPoolExecutor`
  - [ ] Add robust error handling (timeouts, 404s, etc.)
  - [ ] Filter out non-text content (images, PDFs without OCR)

- [ ] **Searcher Node** (`graph/nodes/searcher.py`)
  - [ ] Integrate `search_tool.search_web()`
  - [ ] Query each subtopic's search_query
  - [ ] Store URLs in state (consider adding `search_results` to `ReviewState`)

- [ ] **Fetcher Node** (`graph/nodes/fetcher.py`)
  - [ ] Use `fetch_tool.fetch_multiple()` for efficiency
  - [ ] Create `Document` objects with metadata
  - [ ] Handle fetch failures gracefully (log and continue)

**Resources**:
### Phase 3: RAG Pipeline (Vector Store + Retrieval) **COMPLETED**

**Status**: Full RAG pipeline with FAISS semantic search implemented

**Completed Tasks**:
- [x] **Chunk & Embed Node** (`graph/nodes/chunk_embed.py`)
  - [x] Implemented `RecursiveCharacterTextSplitter` from LangChain
  - [x] Generate embeddings using OpenAI `OpenAIEmbeddings()`
  - [x] Created FAISS index with metadata storage
  - [x] Error handling with fallback to simple chunks

- [x] **Retriever Node** (`graph/nodes/retriever.py`)
  - [x] FAISS similarity search for each subtopic
  - [x] Retrieve top-10 most relevant chunks per subtopic
  - [x] Organize results by subtopic with metadata
  - [x] Fallback to filtering if vector store unavailable

- [x] **Vector Store Utilities** (`vectorstore/__init__.py`)
  - [x] Added `save_vector_store()` for persistence
  - [x] Added `load_vector_store()` for loading saved indexes
  - [x] Added `merge_vector_stores()` for combining indexes

- [x] **Fetcher Node** (`graph/nodes/fetcher.py`)
  - [x] Integrated real URL fetching with `fetch_url()`
  - [x] Create `Document` objects with actual web content
  - [x] Robust error handling with placeholder fallback
  - [x] Content truncation to avoid token limits

**Resources**:
- [LangChain Text Splitters](https://python.langchain.com/docs/modules/data_connection/document_transformers/)
- [FAISS documentation](https://faiss.ai/)
- [LangChain FAISS integration](https://python.langchain.com/docs/integrations/vectorstores/faiss)

---

### Phase 4: Advanced Features **COMPLETED**

**Status**: Advanced features implemented for production use

**Completed Tasks**:
- [x] **Conditional Edges**
  - Added quality check node after fetching
  - Retry logic for failed/insufficient searches
  - Conditional routing based on document count

- [x] **Caching**
  - File-based cache for search results (24-hour expiry)
  - Cache for embeddings to reduce API costs
  - Cache statistics and management utilities
  - Automatic cache invalidation

**Skipped** (Do not have enough time left before the deadline to finish this.):
- [ ] MCP Tools Integration
- [ ] Streaming Output
- [ ] Multi-Agent Collaboration

---

## Implementation Tips

### Starting Point
1. **Begin with Phase 1**: Get LLM calls working with hardcoded data
2. **Test incrementally**: Run `main.py` after each node implementation
3. **Use mock data**: Test graph structure before adding external API calls

### Debugging LangGraph
```python
# Enable verbose logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Print state between nodes
def debug_node(state):
    print(f"Current state: {state}")
    return state

workflow.add_node("debug", debug_node)
```

### Prompt Engineering Tips
- **Be specific**: Clearly define expected output format
- **Provide examples**: Few-shot examples improve consistency
- **Iterate**: Test prompts in OpenAI Playground first
- **System prompts**: Set role and constraints upfront

### Managing Costs
- Use `gpt-3.5-turbo` for development/testing
- Switch to `gpt-4` for final synthesis only
- Cache LLM responses during development
- Set token limits in API calls

---

## State Schema

```python
ReviewState = {
    "topic": str,                    # User's research topic
    "subtopics": List[Subtopic],     # 3-6 planned subtopics
    "documents": List[Document],     # Fetched web pages
    "chunks": List[Dict],            # Chunked & embedded text
    "summaries": List[Summary],      # Per-subtopic summaries
    "final_review": Optional[str],   # Complete literature review
    "vector_store": Optional[FAISS], # FAISS index
}
```

### Pydantic Models

- **`Subtopic`**: `name`, `search_query`, `rationale`
- **`Document`**: `url`, `title`, `content`, `subtopic`
- **`Summary`**: `subtopic`, `summary`, `key_findings`, `sources`

---

## Troubleshooting

### Common Issues

**Graph execution hangs**
- Check for infinite loops in edges
- Ensure all nodes return updated state

**FAISS errors**
- Ensure embeddings have consistent dimensions
- Check that `faiss-cpu` is installed (not `faiss`)

**API rate limits**
- Add sleep/retry logic in search and fetch tools
- Use exponential backoff

**Memory issues with large documents**
- Reduce chunk size
- Process documents in batches
- Use streaming for embeddings

---

## Resources

### LangGraph
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangGraph Tutorials](https://github.com/langchain-ai/langgraph/tree/main/examples)

### LangChain
- [LangChain Docs](https://python.langchain.com/)
- [RAG Tutorial](https://python.langchain.com/docs/use_cases/question_answering/)

### OpenAI
- [API Reference](https://platform.openai.com/docs/api-reference)
- [Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)

---

## Learning Objectives

By completing this project, you'll master:
-  LangGraph state management and graph construction
-  Structured LLM outputs with Pydantic
-  RAG pipeline implementation (chunking, embedding, retrieval)
-  Tool calling patterns
-  Prompt engineering for complex tasks
-  Production-grade error handling and testing

---

## License

MIT License - feel free to extend and adapt!

---

## Current Status

**Project Phase**: Phase 1-4 Complete | Fully Functional Production Agent

**What's Working**:
- **Phase 1**: LLM-powered subtopic planning, summarization, and synthesis
- **Phase 2**: Free DuckDuckGo web search (no API key required)
- **Phase 3**: Full RAG pipeline with FAISS semantic search
  - Document chunking with overlap
  - OpenAI embeddings generation
  - FAISS vector store for semantic retrieval
  - Real web content fetching
- **Phase 4**: Advanced production features
  - Conditional edges with quality checks
  - Automatic search retry on insufficient results
  - File-based caching system (search results & embeddings)
  - Cache expiration (24 hours)
- Complete end-to-end LangGraph workflow

**Next Steps**:
1. Set `OPENAI_API_KEY` environment variable in `.env` file
2. Run `python main.py` to generate a complete literature review
3. The system will:
   - Plan subtopics using GPT-4
   - Search the web with DuckDuckGo (with caching)
   - Check quality and retry if needed
   - Fetch and chunk real web content
   - Create FAISS embeddings for semantic search
   - Retrieve relevant chunks per subtopic
   - Summarize findings with GPT-4
   - Synthesize a complete academic literature review

**Estimated Time to Completion**:
- Phase 1-2: 4-6 hours
- Phase 3: 6-8 hours
---

