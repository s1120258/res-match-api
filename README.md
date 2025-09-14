# 🧠 ResMatch – Advanced AI Career Intelligence Platform

**ResMatch** is a next-generation AI-powered career platform that combines **RAG (Retrieval-Augmented Generation)** and **LangChain autonomous agents** to deliver intelligent job matching, autonomous career strategy planning, and comprehensive skill analysis. Built with production-grade architecture and enterprise-level security.

**🚀 Core Innovation**: RAG-powered market intelligence + LangChain agents for autonomous career planning with advanced AI workflows.

---

## 🔗 Project Overview

- **🌐 Live Application**: [resmatchai.com](https://resmatchai.com/) — Full-stack AI career platform
- **📱 Frontend Repository**: [`res-match-ui`](https://github.com/s1120258/res-match-ui) — React + Vite interface
- **🔄 API Explorer**: [resmatch-api.ddns.net/docs](https://resmatch-api.ddns.net/docs) — Interactive Swagger UI

---

## 🧰 Advanced Tech Stack

| **Layer**           | **Technologies**                             | **Purpose**                                 |
| ------------------- | -------------------------------------------- | ------------------------------------------- |
| **AI/ML Core**      | OpenAI GPT-4o mini, text-embedding-ada-002   | LLM reasoning, vector embeddings            |
| **RAG & Agents**    | LangChain, RAG patterns, Autonomous agents   | Advanced AI workflows, multi-step reasoning |
| **Vector Search**   | Supabase PostgreSQL + pgVector extension     | High-performance similarity search          |
| **Backend API**     | FastAPI, SQLAlchemy, Alembic                 | REST API, ORM, database migrations          |
| **Frontend**        | React, Vite, TypeScript, Chakra UI           | Modern, responsive user interface           |
| **Authentication**  | OAuth2, JWT, bcrypt, Google OAuth            | Secure user authentication                  |
| **Data Processing** | PyPDF2, python-docx, BeautifulSoup4          | Document parsing, web scraping              |
| **Caching**         | In-memory Python dictionaries with TTL       | LLM response caching                        |
| **DevOps**          | Docker, GitHub Actions, GHCR, AWS EC2, NGINX | Containerization, CI/CD, deployment         |
| **Configuration**   | AWS Parameter Store, environment variables   | Secure credential management                |

---

## 📝 Core Features

### 🧠 RAG-Powered Job Analysis

- Market context analysis using similar job retrieval from pgVector database
- Strategic positioning and competitive advantage recommendations
- ~2-3 second comprehensive analysis with market trend synthesis

### 🤖 LangChain Career Strategy Agent

- Autonomous multi-step career planning with specialized tools
- Market analysis, skill gap assessment, and career path planning
- Cost-optimized with token usage tracking and structured JSON output

### 📄 Smart Job & Resume Management

- **Semantic Matching**: pgVector-powered similarity with 85% accuracy correlation
- **Resume Processing**: PDF/DOCX parsing with LLM-powered skill extraction
- **Intelligent Feedback**: Context-aware resume improvement suggestions
- **Application Tracking**: Status management with AI-powered scoring

### 🔒 Security & Infrastructure

- OAuth2 + JWT authentication with Google OAuth integration
- Production-ready with Docker deployment and comprehensive testing

---

## 📁 Documentation

### 📖 Technical Documentation

- **[🧠 TECHNICAL_ARCHITECTURE.md](./docs/TECHNICAL_ARCHITECTURE.md)** — Comprehensive AI/ML system architecture and implementation details
- [📁 API_SPEC.md](./docs/API_SPEC.md) — Complete API reference with AI-powered endpoint descriptions
- [🗂️ DATA_MODEL.md](./docs/DATA_MODEL.md) — Database schema and vector storage specifications

### 🛠️ Development Setup

- [⚙️ SETUP.md](./docs/SETUP.md) — Environment setup and installation guide
- [🧪 TESTING.md](./docs/TESTING.md) — Testing strategies and best practices

---

## 🏆 Technical Highlights

- **🧠 RAG Intelligence**: Market context analysis through similar job retrieval and LLM synthesis
- **🤖 Autonomous Agents**: Multi-tool career strategy planning with specialized analysis tools
- **⚡ High Performance**: ~50ms embeddings, ~1ms similarity search, sub-second API responses
- **🔧 Production Ready**: Docker deployment, CI/CD pipelines, 133+ tests with 100% pass rate
- **🔐 Enterprise Security**: OAuth2/JWT authentication, data protection, secure configuration

**📖 For detailed technical implementation, see [TECHNICAL_ARCHITECTURE.md](./docs/TECHNICAL_ARCHITECTURE.md)**

---

_ResMatch — Next-generation AI career intelligence with RAG-powered insights and autonomous agent planning._
