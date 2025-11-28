# Autonomous Literature Review Agent

A modern AI-powered literature review assistant built with **LangGraph**, **LangChain**, and **OpenAI**, demonstrating cutting-edge agentic AI concepts including RAG, tool calling, and structured outputs.

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

### Phase 1: Core LLM Integration 

**Current Status**: Skeleton with placeholders

**Tasks**:
- [ ] **Planner Node** (`graph/nodes/planner.py`)
  - [ ] Load prompt from `prompts/planner_prompt.txt`
  - [ ] Implement OpenAI structured output API call
  - [ ] Use `SubtopicsPlan` Pydantic model for response parsing
  - [ ] Handle API errors and retries

- [ ] **Summarizer Node** (`graph/nodes/summarizer.py`)
  - [ ] Load prompt template
  - [ ] Format retrieved chunks into prompt
  - [ ] Call OpenAI with structured output (`Summary` model)
  - [ ] Implement token limit handling (chunk splitting if needed)

- [ ] **Synthesizer Node** (`graph/nodes/synthesizer.py`)
  - [ ] Load synthesis prompt
  - [ ] Aggregate all subtopic summaries
  - [ ] Generate comprehensive review with proper structure
  - [ ] Post-process output (formatting, citations)

**Resources**:
- [OpenAI Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs)
- [LangChain ChatOpenAI docs](https://python.langchain.com/docs/integrations/chat/openai)

---

### Phase 2: Search & Fetch Integration

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
- [Brave Search API](https://brave.com/search/api/)
- [SerpAPI](https://serpapi.com/)
- [Trafilatura docs](https://trafilatura.readthedocs.io/)

---

### Phase 3: RAG Pipeline (Vector Store + Retrieval)

**Tasks**:
- [ ] **Chunk & Embed Node** (`graph/nodes/chunk_embed.py`)
  - [ ] Use `RecursiveCharacterTextSplitter` from LangChain
    ```python
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    ```
  - [ ] Generate embeddings:
    - Option A: OpenAI embeddings (`OpenAIEmbeddings()`)
    - Option B: Local models (`HuggingFaceEmbeddings()`)
  - [ ] Create FAISS index:
    ```python
    from langchain_community.vectorstores import FAISS
    vector_store = FAISS.from_texts(texts, embeddings, metadatas=metadatas)
    ```
  - [ ] Store `vector_store` in state

- [ ] **Retriever Node** (`graph/nodes/retriever.py`)
  - [ ] For each subtopic, query vector store:
    ```python
    results = vector_store.similarity_search(query, k=10)
    ```
  - [ ] Organize retrieved chunks by subtopic
  - [ ] Consider re-ranking (e.g., with cross-encoder) for better relevance

- [ ] **Vector Store Utilities** (`vectorstore/__init__.py`)
  - [ ] Add persistence functions:
    ```python
    vector_store.save_local("path/to/index")
    FAISS.load_local("path/to/index", embeddings)
    ```
  - [ ] Add helper for incremental updates

**Resources**:
- [LangChain Text Splitters](https://python.langchain.com/docs/modules/data_connection/document_transformers/)
- [FAISS documentation](https://faiss.ai/)
- [LangChain FAISS integration](https://python.langchain.com/docs/integrations/vectorstores/faiss)

---

### Phase 4: Advanced Features (Optional)

- [ ] **Conditional Edges**
  - Add quality checks (e.g., if too few documents, retry search)
  - Implement feedback loops

- [ ] **MCP Tools Integration**
  - Research Model Context Protocol
  - Add MCP-compatible tool interfaces

- [ ] **Streaming Output**
  - Stream LLM responses for real-time feedback
  - Add progress indicators

- [ ] **Caching**
  - Cache search results to avoid redundant API calls
  - Cache embeddings for reused documents

- [ ] **Multi-Agent Collaboration**
  - Add specialist agents (e.g., "methodology critic", "trend analyzer")
  - Implement agent communication protocol

---

### Phase 5: Production Readiness

- [ ] **Error Handling**
  - Comprehensive try-except blocks in all nodes
  - Graceful degradation (continue with partial results)
  - Logging with `logging` module

- [ ] **Configuration Management**
  - Create `config.yaml` for parameters (chunk size, k-value, etc.)
  - Environment-based configs (dev/prod)

- [ ] **Testing**
  - Unit tests for each node
  - Integration test for full graph
  - Mock API responses for testing

- [ ] **CLI Interface**
  - Add `argparse` for command-line arguments
  - Support for batch processing multiple topics
  - Output format options (Markdown, PDF, JSON)

- [ ] **Documentation**
  - Add docstrings to all functions
  - Create usage examples
  - Add troubleshooting guide

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

## 🔧 Troubleshooting

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

##  Current Status

**Project Phase**: Skeleton

**Next Steps**:
1. Set up OpenAI API key
2. Implement Phase 1 (LLM integration in planner node)
3. Test with simple topic before adding search

**Estimated Time to Completion**:
- Phase 1-2: 4-6 hours
- Phase 3: 6-8 hours
- Phase 4-5: 8-12 hours 

---

**Questions or issues?** Open an issue or consult the LangGraph community!
