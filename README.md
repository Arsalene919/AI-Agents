# 🤖 AI Agents project

> A collection of 5 AI agent projects built with OpenAI API, from beginner to production-ready.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-green?logo=openai)
![Streamlit](https://img.shields.io/badge/Streamlit-deployed-red?logo=streamlit)
![FastAPI](https://img.shields.io/badge/FastAPI-REST_API-009688?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)
![MCP](https://img.shields.io/badge/MCP-Custom_Server-8A2BE2)

---

## 📌 Overview

This repository demonstrates core AI agent concepts, **tool use, function calling, RAG, memory, and multi-step pipelines**, through 5 progressively complex projects.

| # | Project | Key Concept | Stack |
|---|---------|-------------|-------|
| 1 | 🔍 Web Search Agent | Tool use + web search | OpenAI + Tavily |
| 2 | 🧮 Calculator Agent | Custom function calling | OpenAI + Python |
| 3 | 📄 Document Analyst | RAG + context injection | OpenAI + PyPDF2 |
| 4 | 🤖 Personal Assistant | Multi-tools + memory | OpenAI + Weather API + Tavily |
| 5 | 🔬 Research Assistant | Multi-step pipeline + UI | OpenAI + Streamlit | + OAuth |
| 6 | ⚙️ Backend API | JWT auth, ORM, persistence | FastAPI + SQLAlchemy + PostgreSQL |
| 7 | 🔌 MCP Server | Model Context Protocol tools | MCP SDK + httpx |
---

## Getting Started

### Prerequisites

```bash
python 3.10+
- Docker Desktop
- API keys: [OpenAI](https://platform.openai.com) · [Tavily](https://tavily.com) *(1000 free searches/month)*
```

### Environment Variables

Create a `.env` file at the root of the project:

```env
OPENAI_API_KEY=sk-...
TAVILY_API_KEY=tvly-...
OPENWEATHER_API_KEY=...
JWT_SECRET_KEY=... 
```
> Generate a secure JWT secret:
 
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

> Get your keys:
> - OpenAI → [platform.openai.com](https://platform.openai.com)
> - Tavily → [tavily.com](https://tavily.com) *(1000 free searches/month)*
> - OpenWeather → [openweathermap.org](https://openweathermap.org/api) *(free tier)*

---

## Project Structure

```
ai-agents-portfolio/
│
├── 01_web_search_agent/
│   └── websearchagents.py              # Web search agent with Tavily
│
├── 02_calculator_agent/
│   └── intelligentCalculator.py              # Function calling with safe eval
│
├── 03_document_analyst/
│   ├── pdfReader.py              # PDF Q&A agent
│   └── sample.pdf            # Test document
│
├── 04_personal_assistant/
│   └── agent.py              # Multi-tool agent with memory
│
├── 05_research_assistant/            # Streamlit frontend
│   ├── ResearchAssistant.py          # Main app + PDF export
│   ├── auth_client.py                # Login / register screens
│   ├── api_client.py                 # Authenticated API calls
│   ├── drive_export.py               # Google Drive OAuth upload
│   └── requirements.txt
│
├── 06_fastapi_backend/               # Production REST API
│   ├── main.py                       # Routes
│   ├── auth.py                       # JWT + password hashing
│   ├── models.py                     # SQLAlchemy models (User, Report)
│   ├── schemas.py                    # Pydantic validation
│   ├── services.py                   # OpenAI + Tavily logic
│   ├── database.py                   # PostgreSQL connection
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── requirements.txt
│
├──  07_mcp_server/                    # Custom MCP server
|   ├── server.py                     # 3 tools exposed via MCP
|   └── config.example.json           # MCP client config template
|
|
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Project 1: Web Search Agent

The agent receives a question, searches the web, and returns a summarized answer.

**Concepts:** tool use, prompt engineering, API chaining

```bash
cd 01_web_search_agent
python websearchagents.py
```

**Key idea:** The LLM doesn't answer from memory, it calls a real search tool and grounds its response in fresh data.

---

## Project 2: Calculator Agent

The agent detects math problems and delegates computation to a real Python function, eliminating hallucinations.

**Concepts:** function calling, safe code execution, tool routing

```bash
cd 02_calculator_agent
python intelligentCalculator.py
```

**Key idea:** LLMs are bad at math. By offloading calculations to a Python function, the agent is always accurate.

---

## Project 3: Document Analyst

Upload a PDF and ask questions about it. The agent reads the document and answers based strictly on its content.

**Concepts:** RAG (Retrieval-Augmented Generation), context injection, knowledge grounding

```bash
cd 03_document_analyst
python pdfReader.py
```

**Key idea:** Instead of relying on training data, the agent uses your document as its knowledge source, which is the foundation of enterprise RAG systems.

---

## Project 4: Personal Assistant

A conversational agent that autonomously selects from multiple tools: weather, web search, or calculator, and remembers the full conversation.

**Concepts:** multi-tool agents, autonomous tool selection, conversational memory

```bash
cd 04_personal_assistant
python agent.py
```

**Key idea:** The agent reasons about *which* tool to use based on the user's intent, which is the core of autonomous AI agents.

---

## Project 5: Research Assistant *(deployed)*

The most complete project: a full pipeline that searches the web, analyzes sources, and writes a structured report with a Streamlit UI. Reports are stored per user and can be downloaded as PDF or Markdown, or saved directly to the user's Google Drive.
 
**Concepts:** multi-step agent pipeline, JWT authentication, OAuth 2.0, PDF generation


```bash
cd 05_research_assistant
streamlit run ResearchAssistant.py
```

**Live demo:** [ai-agents.streamlit.app](https://ai-agents-lphtojmdc7avvhccti6zdq.streamlit.app/) ← update after deployment

---

## Project 6: Backend API
 
A production-grade REST API with authentication and persistent storage.
 
```bash
cd 06_fastapi_backend
docker-compose up --build
```
 
### Endpoints
 
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/auth/register` | — | Create an account |
| `POST` | `/auth/login` | — | Get a JWT access token |
| `GET` | `/auth/me` | 🔒 | Current user info |
| `POST` | `/reports/generate` | 🔒 | Generate and store a report |
| `GET` | `/reports` | 🔒 | List your reports |
| `GET` | `/reports/search/query?q=` | 🔒 | Search your reports |
| `GET` | `/reports/{id}` | 🔒 | Get one of your reports |
| `DELETE` | `/reports/{id}` | 🔒 | Delete one of your reports |

---

## Project 7: MCP Server
 
A custom Model Context Protocol server that exposes the platform's capabilities to any MCP client, such as Claude Desktop or the MCP Inspector.
 
| Tool | Description |
|------|-------------|
| `save_report` | Generates and stores a research report via the API |
| `search_reports` | Searches existing reports |
| `export_to_drive` | Exports a report to Google Drive |
 
**Setup:**
 
```bash
cd 07_mcp_server
cp config.example.json config.json
# Add your tokens to config.json (gitignored)
npx @modelcontextprotocol/inspector python server.py
```
 
**Key idea:** MCP standardizes how agents access tools. Instead of writing custom integrations for every client, one server exposes the same tools to any MCP-compatible agent.
 
---

## Concepts Covered

- **Tool Use / Function Calling** : Making LLMs interact with external systems
- **RAG** : Grounding LLM responses in external documents
- **Agent Memory** : Maintaining conversation context across turns
- **Multi-step Pipelines** : Chaining agent actions to complete complex tasks
- **Safe Code Execution** : Running model-generated expressions securely
- **REST API Design** : Route ordering, response models, Pydantic validation
- **Authentication** : JWT tokens, password hashing, per-user data isolation
- **OAuth 2.0** : Delegated access to users' Google Drive accounts
- **Database Persistence** : SQLAlchemy ORM, relationships, Docker volumes
- **Model Context Protocol** : Custom server exposing standardized tools
- **Containerization** : Multi-service orchestration with Docker Compose
---
 
## Security
 
- All API keys live in `.env` (gitignored)
- MCP tokens live in `config.json` (gitignored), with `config.example.json` as a committed template
- Passwords are SHA-256 pre-hashed then bcrypt-hashed, removing bcrypt's 72-byte limit without truncating
- Every protected route filters by the authenticated user's ID, so users cannot read each other's reports
- Streamlit secrets and Docker environment variables keep credentials out of the codebase


---
