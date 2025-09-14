# 🧠 ResMatch – Advanced AI Career Intelligence Platform

**ResMatch** is a next-generation AI-powered career platform that combines **RAG (Retrieval-Augmented Generation)**, **LangChain autonomous agents**, and **multi-language AI** to deliver intelligent job matching, autonomous career strategy planning, and comprehensive skill analysis. Built with production-grade architecture and enterprise-level security.

**🚀 Core Innovation**: RAG-powered market intelligence + LangChain agents for autonomous career planning with Japanese/English multi-language support.

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
| **Multi-language**  | Auto-detection, explicit language parameters | Japanese/English AI responses               |
| **Caching**         | In-memory Python dictionaries with TTL       | LLM response caching                        |
| **DevOps**          | Docker, GitHub Actions, GHCR, AWS EC2, NGINX | Containerization, CI/CD, deployment         |
| **Configuration**   | AWS Parameter Store, environment variables   | Secure credential management                |

---

## 🚀 Advanced AI Features

### 🧠 RAG-Powered Intelligent Job Analysis

- **Market Context Analysis**: Retrieves similar jobs from pgVector database to provide market intelligence
- **Strategic Positioning**: Competitive advantage recommendations based on similar role analysis
- **Performance**: ~2-3 second comprehensive analysis with market trend synthesis
- **Multi-language Support**: Automatic Japanese/English detection with culturally-adapted responses

### 🤖 LangChain Autonomous Career Strategy Agent

- **Multi-tool Orchestration**: Specialized tools for job market analysis, skill assessment, and career planning
- **Autonomous Reasoning**: Multi-step decision making with 5-iteration limit for comprehensive analysis
- **Cost Optimization**: Token usage tracking and intelligent prompt management
- **Structured Output**: JSON + narrative responses with actionable recommendations

#### Agent Specialized Tools:

1. **JobAnalysisTool**: Market trends, demand analysis, and salary insights with Japan market focus
2. **SkillGapAnalysisTool**: Current skills vs. target requirements with learning path recommendations
3. **CareerPathPlannerTool**: Multi-phase career progression with measurable success metrics

### 💡 Core Platform Features

#### ✅ Enhanced Job Search & Management

- **Smart Matching**: pgVector-powered semantic similarity with 85% human judgment correlation
- **External Integration**: RemoteOK and other job board scraping with real-time updates
- **Application Tracking**: Status management with AI-powered match scoring

#### 📄 Advanced Resume Management

- **Multi-format Support**: PDF/DOCX parsing with automated text extraction
- **Skill Extraction**: LLM-powered skill identification with confidence scoring
- **Dynamic Feedback**: Context-aware resume improvement suggestions
- **Vector Storage**: 1536-dimensional embeddings for semantic matching

#### 🎯 Intelligent Skill Analysis

- **LLM-based Normalization**: Dynamic skill standardization (e.g., "JS" → "JavaScript")
- **Semantic Matching**: Beyond exact string matching for transferable skills
- **Learning Recommendations**: Prioritized skill development with time estimates
- **Gap Analysis**: Current vs. target role skill comparison with actionable insights

#### 🌐 Multi-Language AI Support

- **Auto-Detection**: Unicode range analysis for Japanese character recognition
- **Explicit Control**: `response_language` parameter support across all AI endpoints
- **Cultural Adaptation**: Japan-specific market insights and business culture considerations
- **Full Coverage**: Both RAG and Agent systems support Japanese/English responses

#### 📊 Analytics & Insights

- **Performance Metrics**: Real-time API response times and token usage tracking
- **User Analytics**: Application patterns, skill development trends, and success metrics
- **Market Intelligence**: Industry trend analysis and competitive positioning

#### 🔒 Enterprise-Grade Security

- **OAuth2 + JWT**: Secure token-based authentication with refresh capability
- **Google OAuth Integration**: Unified authentication flow with automatic account linking
- **Data Protection**: bcrypt password hashing, SQL injection prevention, CORS configuration
- **Secure Configuration**: AWS Parameter Store integration for credential management

---

## 🌐 API Endpoints Overview

### 🧠 RAG-Powered Intelligent Analysis

- `GET /api/v1/jobs/{job_id}/intelligent-analysis` — Comprehensive job analysis with market context
- `GET /api/v1/jobs/{job_id}/market-intelligence` — Market intelligence analysis only
- `GET /api/v1/health/intelligent-matching` — RAG service health check

### 🤖 LangChain Career Strategy Agent

- `POST /api/v1/career/strategy-planning` — Autonomous multi-step career strategy planning
- `POST /api/v1/career/skill-gap-analysis` — AI-powered skill gap assessment
- `GET /api/v1/career/market-insights` — Job market insights for career planning
- `GET /api/v1/career/agent-status` — Agent service health and capabilities

### 📊 Core Platform APIs

- `GET /api/v1/jobs/search` — Semantic job search with vector similarity
- `POST /api/v1/resumes/upload` — Resume upload with AI skill extraction
- `GET /api/v1/resume/skills` — LLM-powered skill analysis and normalization
- `POST /api/v1/auth/google/verify` — Unified Google OAuth authentication

**🔄 Interactive API Documentation**: [resmatch-api.ddns.net/docs](https://resmatch-api.ddns.net/docs)

---

## 📁 Documentation

### 📖 Technical Documentation

- **[🧠 TECHNICAL_ARCHITECTURE.md](./docs/TECHNICAL_ARCHITECTURE.md)** — Comprehensive AI/ML system architecture and implementation details
- **[🤖 RAG_AGENT_IMPLEMENTATION.md](./docs/RAG_AGENT_IMPLEMENTATION.md)** — RAG & LangChain agent implementation guide and planning
- [📁 API_SPEC.md](./docs/API_SPEC.md) — Complete API reference with AI-powered endpoint descriptions
- [🗂️ DATA_MODEL.md](./docs/DATA_MODEL.md) — Database schema and vector storage specifications

### 🛠️ Development Setup

- [⚙️ SETUP.md](./docs/SETUP.md) — Environment setup and installation guide
- [🧪 TESTING.md](./docs/TESTING.md) — Testing strategies and best practices

---

## 🏆 Technical Achievements & Performance

### 🎯 Performance Metrics

| **Operation**          | **Latency** | **Throughput** | **Optimization**         |
| ---------------------- | ----------- | -------------- | ------------------------ |
| Vector Embedding       | ~50ms       | 20 RPS         | OpenAI API limits        |
| Similarity Calculation | ~1ms        | 1000+ RPS      | Pure Python computation  |
| LLM Text Generation    | 2-5s        | Variable       | Token-based optimization |
| Database Queries       | 5-20ms      | 500+ RPS       | pgVector indexing        |
| RAG Analysis           | 2-3s        | 10-15 RPS      | Context-aware retrieval  |
| Agent Workflow         | 8-12s       | 5-8 RPS        | Multi-tool orchestration |
| Language Detection     | <1ms        | 10000+ RPS     | Unicode range analysis   |

### 🚀 Innovation Highlights

- **🧠 RAG Intelligence**: Market context analysis through similar job retrieval and LLM synthesis
- **🤖 Autonomous Agents**: Multi-tool career strategy planning with specialized analysis tools
- **🌐 Multi-Language AI**: Japanese/English support with automatic detection and cultural adaptation
- **⚡ Cost-Optimized AI**: Strategic model selection, token management, and response caching
- **📊 Vector-Powered Search**: High-performance semantic job matching with pgVector optimization
- **🎯 Technical Specialization**: AI/RAG/LLM focused career guidance with Japan market insights

### 🏢 Engineering Excellence

- **🏗️ Clean Architecture**: Service-oriented design with clear separation of concerns
- **🧪 Comprehensive Testing**: 133+ tests with 100% pass rate, extensive AI feature coverage
- **🚀 Production Ready**: Docker deployment with enterprise-grade CI/CD pipelines
- **🔐 Security Implementation**: Industry-standard authentication, authorization, and data protection
- **📊 Monitoring & Observability**: Comprehensive logging, performance tracking, and health checks

### 🎪 DevOps & Deployment Excellence

- **📦 Multi-Platform Builds**: linux/amd64 and linux/arm64 support with GitHub Container Registry
- **🎯 Smart Deployment**: Change-detection based deployment with automated health verification
- **🛡️ Security**: SSL/TLS with Let's Encrypt, secure headers, environment variable management
- **⚡ Performance Optimization**: Native ARM64 platform, connection pooling, caching strategies
- **🔍 Health Monitoring**: Real-time health checks with automated rollback capability

**📖 For detailed technical implementation, see [TECHNICAL_ARCHITECTURE.md](./docs/TECHNICAL_ARCHITECTURE.md)**

---

_ResMatch — Next-generation AI career intelligence with RAG-powered insights and autonomous agent planning._
