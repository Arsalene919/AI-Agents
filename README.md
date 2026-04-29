# 🤖 AI Agents project

> A collection of 5 AI agent projects built with OpenAI API — from beginner to production-ready.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-green?logo=openai)
![Streamlit](https://img.shields.io/badge/Streamlit-deployed-red?logo=streamlit)

---

## 📌 Overview

This repository demonstrates core AI agent concepts — **tool use, function calling, RAG, memory, and multi-step pipelines**, through 5 progressively complex projects.

| # | Project | Key Concept | Stack |
|---|---------|-------------|-------|
| 1 | 🔍 Web Search Agent | Tool use + web search | OpenAI + Tavily |
| 2 | 🧮 Calculator Agent | Custom function calling | OpenAI + Python |
| 3 | 📄 Document Analyst | RAG + context injection | OpenAI + PyPDF2 |
| 4 | 🤖 Personal Assistant | Multi-tools + memory | OpenAI + Weather API + Tavily |
| 5 | 🔬 Research Assistant | Multi-step pipeline + UI | OpenAI + Streamlit |

---

## Getting Started

### Prerequisites

```bash
python 3.10+
pip install openai requests PyPDF2 streamlit tavily-python
```

### Environment Variables

Create a `.env` file at the root of the project:

```env
OPENAI_API_KEY=sk-...
TAVILY_API_KEY=tvly-...
OPENWEATHER_API_KEY=...
```

> Get your keys:
> - OpenAI → [platform.openai.com](https://platform.openai.com)
> - Tavily → [tavily.com](https://tavily.com) *(1000 free searches/month)*
> - OpenWeather → [openweathermap.org](https://openweathermap.org/api) *(free tier)*

---

## 📁 Project Structure

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
├── 05_research_assistant/
│   └── ResearchAssistant.py                # Full Streamlit app
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Project 1 — Web Search Agent

The agent receives a question, searches the web, and returns a summarized answer.

**Concepts:** tool use, prompt engineering, API chaining

```bash
cd 01_web_search_agent
python websearchagents.py
```

**Key idea:** The LLM doesn't answer from memory, it calls a real search tool and grounds its response in fresh data.

---

## Project 2 — Calculator Agent

The agent detects math problems and delegates computation to a real Python function, eliminating hallucinations.

**Concepts:** function calling, safe code execution, tool routing

```bash
cd 02_calculator_agent
python intelligentCalculator.py
```

**Key idea:** LLMs are bad at math. By offloading calculations to a Python function, the agent is always accurate.

---

## Project 3 — Document Analyst

Upload a PDF and ask questions about it. The agent reads the document and answers based strictly on its content.

**Concepts:** RAG (Retrieval-Augmented Generation), context injection, knowledge grounding

```bash
cd 03_document_analyst
python pdfReader.py
```

**Key idea:** Instead of relying on training data, the agent uses your document as its knowledge source, which is the foundation of enterprise RAG systems.

---

## Project 4 — Personal Assistant

A conversational agent that autonomously selects from multiple tools: weather, web search, or calculator, and remembers the full conversation.

**Concepts:** multi-tool agents, autonomous tool selection, conversational memory

```bash
cd 04_personal_assistant
python agent.py
```

**Key idea:** The agent reasons about *which* tool to use based on the user's intent, which is the core of autonomous AI agents.

---

## Project 5 — Research Assistant *(deployed)*

The most complete project: a full pipeline that searches the web, analyzes sources, and writes a structured report with a Streamlit UI.

**Concepts:** multi-step agent pipeline, Streamlit UI, report generation

```bash
cd 05_research_assistant
streamlit run ResearchAssistant.py
```

**Live demo:** [ai-agents.streamlit.app](https://ai-agents-lphtojmdc7avvhccti6zdq.streamlit.app/) ← update after deployment

---

## Concepts Covered

- **Tool Use / Function Calling** : Making LLMs interact with external systems
- **RAG** : Grounding LLM responses in external documents
- **Agent Memory** : Maintaining conversation context across turns
- **Multi-step Pipelines** : Chaining agent actions to complete complex tasks
- **Safe Code Execution** : Running model-generated expressions securely

---

## requirements.txt

```
openai>=1.0.0
requests>=2.31.0
PyPDF2>=3.0.0
streamlit>=1.32.0
tavily-python>=0.3.0
python-dotenv>=1.0.0
```

---
