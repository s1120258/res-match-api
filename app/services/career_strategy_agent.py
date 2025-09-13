"""
LangChain-based career strategy agent service.
Provides multi-step autonomous career planning and analysis using agent patterns.
"""

import json
import logging
from typing import Dict, List, Any, Optional, Tuple, Union
from uuid import UUID
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain.tools import BaseTool, tool
from langchain.memory import ConversationBufferMemory
from langchain_community.callbacks.manager import get_openai_callback

from app.services.embedding_service import embedding_service
from app.services.llm_service import llm_service
from app.services.similarity_service import similarity_service
from app.crud.job import get_jobs
from app.crud.resume import get_resume_by_user
from app.core.config import settings

logger = logging.getLogger(__name__)


class CareerStrategyAgentError(Exception):
    """Exception raised when career strategy agent operations fail."""

    pass


class JobAnalysisTool(BaseTool):
    """Tool for analyzing job market trends and opportunities."""

    name: str = "job_analysis_tool"
    description: str = """
    Analyze job market trends and opportunities for career planning.
    Input should be a JSON string with keys: user_id, target_roles, location_preference.
    Returns market analysis including demand trends, salary insights, and skill requirements.
    """
    db: Union[Session, Any]

    def __init__(self, db: Session):
        super().__init__(db=db)

    def _run(self, query: str) -> str:
        """Execute job market analysis."""
        try:
            # Parse input
            query_data = json.loads(query)
            user_id = query_data.get("user_id")
            target_roles = query_data.get("target_roles", [])
            location_preference = query_data.get("location_preference", "")

            # Get user's job postings for market context
            user_jobs = get_jobs(self.db, UUID(user_id))[:50]

            if not user_jobs:
                return json.dumps(
                    {
                        "market_analysis": "Limited market data available - no job postings found",
                        "demand_trends": ["Insufficient data for trend analysis"],
                        "salary_insights": "No salary data available",
                        "skill_requirements": ["General industry skills recommended"],
                    }
                )

            # Analyze job market trends from user's posted jobs
            job_titles = [job.title for job in user_jobs if job.title]
            job_descriptions = [job.description for job in user_jobs if job.description]

            # Create market analysis prompt
            market_prompt = f"""
            DETAILED TECHNICAL MARKET ANALYSIS FOR AI/RAG SPECIALIZATION

            TARGET ROLES: {', '.join(target_roles) if target_roles else 'General analysis'}
            LOCATION PREFERENCE: {location_preference or 'Not specified'}
            SPECIALIZATION FOCUS: AI Agents, RAG systems, LLM integration, Python/FastAPI backend

            AVAILABLE JOB DATA:
            Job Titles: {job_titles[:10]}  # Limit to first 10 for prompt size

            CRITICAL ANALYSIS REQUIREMENTS:
            1. Identify SPECIFIC companies in Japan hiring for AI/RAG roles
            2. Provide ACTUAL salary ranges in JPY (not generic statements)
            3. List SPECIFIC technical requirements: Python frameworks, vector DB experience, LLM APIs
            4. Analyze remote work policies for AI roles in Japanese companies
            5. Reference SPECIFIC technologies: LangChain, pgvector, FastAPI, AWS, OpenAI API

            Provide DETAILED analysis in JSON format:
            {{
                "market_analysis": "Specific market conditions for AI/RAG roles in Japan with company examples",
                "demand_trends": ["Specific trend with technology names", "Remote work adoption in Japan AI sector", "LLM integration demand growth"],
                "salary_insights": "Actual JPY ranges: Junior 6M-8M, Senior 10M-15M, Lead 15M+ (adjust with real data)",
                "skill_requirements": ["LangChain framework experience", "pgvector/ChromaDB proficiency", "FastAPI + Pydantic", "RAG architecture design", "LLM prompt engineering"]
            }}
            """

            # Use existing LLM service for analysis
            analysis_result = llm_service.generate_feedback(
                resume_text=market_prompt, feedback_type="general"
            )

            if analysis_result and analysis_result[0]:
                try:
                    # Try to extract JSON from the response
                    response_text = analysis_result[0]
                    if "{" in response_text and "}" in response_text:
                        json_start = response_text.find("{")
                        json_end = response_text.rfind("}") + 1
                        json_str = response_text[json_start:json_end]
                        parsed_result = json.loads(json_str)
                        return json.dumps(parsed_result)
                except json.JSONDecodeError:
                    pass

            # Fallback response if JSON parsing fails
            return json.dumps(
                {
                    "market_analysis": f"Market analysis for {len(user_jobs)} job opportunities",
                    "demand_trends": [
                        "Technology roles in high demand",
                        "Remote work opportunities increasing",
                    ],
                    "salary_insights": "Competitive salary ranges observed across postings",
                    "skill_requirements": [
                        "Technical skills",
                        "Communication abilities",
                        "Problem-solving",
                    ],
                }
            )

        except Exception as e:
            logger.error(f"Error in job analysis tool: {str(e)}")
            return json.dumps(
                {
                    "error": f"Analysis failed: {str(e)}",
                    "market_analysis": "Unable to complete market analysis",
                    "demand_trends": ["Analysis unavailable"],
                    "salary_insights": "No salary insights available",
                    "skill_requirements": ["General skills recommended"],
                }
            )


class SkillGapAnalysisTool(BaseTool):
    """Tool for analyzing skill gaps and learning recommendations."""

    name: str = "skill_gap_analysis_tool"
    description: str = """
    Analyze skill gaps between current profile and target career goals.
    Input should be a JSON string with keys: user_id, target_roles, career_goals.
    Returns skill gap analysis and learning recommendations.
    """
    db: Union[Session, Any]

    def __init__(self, db: Session):
        super().__init__(db=db)

    def _run(self, query: str) -> str:
        """Execute skill gap analysis."""
        try:
            # Parse input
            query_data = json.loads(query)
            user_id = query_data.get("user_id")
            target_roles = query_data.get("target_roles", [])
            career_goals = query_data.get("career_goals", "")

            # Get user's resume for current skills
            user_resume = get_resume_by_user(self.db, UUID(user_id))

            if not user_resume or not user_resume.extracted_text:
                return json.dumps(
                    {
                        "current_skills": ["Unable to analyze - no resume data"],
                        "skill_gaps": ["Complete skills assessment needed"],
                        "learning_recommendations": [
                            "Upload resume for personalized recommendations"
                        ],
                        "priority_skills": ["Basic professional skills"],
                    }
                )

            # Create skill gap analysis prompt
            skill_prompt = f"""
            TECHNICAL SKILL GAP ANALYSIS FOR AI/RAG SPECIALIZATION

            CURRENT PROFILE:
            {user_resume.extracted_text[:1000]}...

            TARGET ROLES: {', '.join(target_roles) if target_roles else 'General career growth'}
            CAREER GOALS: {career_goals or 'Professional development'}

            SPECIALIZATION REQUIREMENTS: AI Agents, RAG systems, LLM integration, Python/FastAPI

            CRITICAL ANALYSIS REQUIREMENTS:
            1. Identify SPECIFIC technical skills present in resume (Python, frameworks, databases, cloud)
            2. Pinpoint EXACT technology gaps for AI/RAG roles (LangChain, vector DBs, LLM APIs)
            3. Provide CONCRETE learning paths with specific courses/certifications
            4. Reference SPECIFIC technologies: pgvector, ChromaDB, Pinecone, OpenAI API, Anthropic Claude
            5. Include project-based learning recommendations with technology stacks

            Provide TECHNICAL skill gap analysis in JSON format:
            {{
                "current_skills": ["Python programming (X years)", "FastAPI framework experience", "PostgreSQL database management"],
                "skill_gaps": ["LangChain framework proficiency", "Vector database implementation (pgvector/Pinecone)", "RAG architecture design", "LLM prompt engineering"],
                "learning_recommendations": ["Complete LangChain course by Harrison Chase", "Build RAG system with pgvector tutorial", "AWS Bedrock certification for LLM deployment"],
                "priority_skills": ["LangChain Agent development", "Production RAG implementation", "Vector similarity search optimization"]
            }}
            """

            # Use LLM service with general feedback type for skill analysis
            analysis_result = llm_service.generate_feedback(
                resume_text=skill_prompt, feedback_type="general"
            )

            if analysis_result and analysis_result[0]:
                try:
                    # Try to extract JSON from the response
                    response_text = analysis_result[0]
                    if "{" in response_text and "}" in response_text:
                        json_start = response_text.find("{")
                        json_end = response_text.rfind("}") + 1
                        json_str = response_text[json_start:json_end]
                        parsed_result = json.loads(json_str)
                        return json.dumps(parsed_result)
                except json.JSONDecodeError:
                    pass

            # Fallback response
            return json.dumps(
                {
                    "current_skills": [
                        "Professional experience demonstrated",
                        "Communication skills",
                        "Technical abilities",
                    ],
                    "skill_gaps": [
                        "Specific technical skills for target role",
                        "Industry-specific knowledge",
                    ],
                    "learning_recommendations": [
                        "Focus on target role requirements",
                        "Build portfolio projects",
                    ],
                    "priority_skills": [
                        "Role-specific technical skills",
                        "Industry best practices",
                    ],
                }
            )

        except Exception as e:
            logger.error(f"Error in skill gap analysis tool: {str(e)}")
            return json.dumps(
                {
                    "error": f"Analysis failed: {str(e)}",
                    "current_skills": ["Unable to analyze"],
                    "skill_gaps": ["Analysis unavailable"],
                    "learning_recommendations": ["Retry analysis with valid data"],
                    "priority_skills": ["General professional development"],
                }
            )


class CareerPathPlannerTool(BaseTool):
    """Tool for creating structured career progression plans."""

    name: str = "career_path_planner_tool"
    description: str = """
    Create structured career progression plans with timelines and milestones.
    Input should be a JSON string with keys: current_role, target_role, timeframe, constraints.
    Returns detailed career progression plan with actionable steps.
    """

    def _run(self, query: str) -> str:
        """Execute career path planning."""
        try:
            # Parse input
            query_data = json.loads(query)
            current_role = query_data.get("current_role", "Current Position")
            target_role = query_data.get("target_role", "Target Position")
            timeframe = query_data.get("timeframe", "2-3 years")
            constraints = query_data.get("constraints", [])

            # Create career planning prompt
            planning_prompt = f"""
            TECHNICAL CAREER PROGRESSION PLAN FOR AI/RAG SPECIALIZATION

            FROM: {current_role}
            TO: {target_role}
            TIMEFRAME: {timeframe}
            TECHNICAL FOCUS: AI Agents, RAG systems, LLM integration, Python/FastAPI backend
            CONSTRAINTS: {', '.join(constraints) if constraints else 'None specified'}

            CRITICAL PLANNING REQUIREMENTS:
            1. Create CONCRETE learning milestones with specific technologies
            2. Define MEASURABLE skill acquisition goals (certifications, projects)
            3. Include SPECIFIC project recommendations using target tech stack
            4. Reference ACTUAL courses, tutorials, and resources
            5. Plan for REAL portfolio projects demonstrating capabilities

            Provide TECHNICAL career plan in JSON format:
            {{
                "career_phases": [
                    {{
                        "phase": "Phase 1: Foundation Building (Months 1-6)",
                        "objectives": ["Master LangChain Agent development", "Implement first RAG system"],
                        "key_actions": ["Complete LangChain course + build 3 agent projects", "Deploy RAG app with pgvector on AWS", "Contribute to open-source AI projects"],
                        "success_metrics": ["2 RAG projects in portfolio", "LangChain certification", "1000+ GitHub stars on AI project"]
                    }}
                ],
                "key_milestones": ["First production RAG deployment", "Technical leadership role transition", "AI conference speaking opportunity"],
                "potential_challenges": ["Keeping up with rapid AI tool evolution", "Competition from experienced ML engineers", "Scaling from individual contributor to team lead"],
                "success_strategies": ["Build in public on Twitter/LinkedIn", "Create technical content (blogs/videos)", "Network at AI meetups in Japan", "Mentor junior developers"]
            }}
            """

            # Use existing LLM service for planning
            planning_result = llm_service.generate_feedback(
                resume_text=planning_prompt, feedback_type="general"
            )

            if planning_result and planning_result[0]:
                try:
                    # Try to extract JSON from the response
                    response_text = planning_result[0]
                    if "{" in response_text and "}" in response_text:
                        json_start = response_text.find("{")
                        json_end = response_text.rfind("}") + 1
                        json_str = response_text[json_start:json_end]
                        parsed_result = json.loads(json_str)
                        return json.dumps(parsed_result)
                except json.JSONDecodeError:
                    pass

            # Fallback structured plan
            return json.dumps(
                {
                    "career_phases": [
                        {
                            "phase": "Phase 1 (Short-term: 6 months)",
                            "objectives": ["Skill development", "Network building"],
                            "key_actions": [
                                "Complete relevant training",
                                "Join professional groups",
                            ],
                            "success_metrics": [
                                "Certifications earned",
                                "Connections made",
                            ],
                        },
                        {
                            "phase": "Phase 2 (Medium-term: 1-2 years)",
                            "objectives": ["Gain experience", "Build portfolio"],
                            "key_actions": [
                                "Take on stretch projects",
                                "Document achievements",
                            ],
                            "success_metrics": [
                                "Project success",
                                "Skill demonstration",
                            ],
                        },
                    ],
                    "key_milestones": [
                        f"Transition from {current_role} to {target_role}",
                        "Skill mastery achievement",
                    ],
                    "potential_challenges": [
                        "Market competition",
                        "Skill acquisition time",
                    ],
                    "success_strategies": [
                        "Consistent learning",
                        "Strategic networking",
                        "Performance excellence",
                    ],
                }
            )

        except Exception as e:
            logger.error(f"Error in career path planner tool: {str(e)}")
            return json.dumps(
                {
                    "error": f"Planning failed: {str(e)}",
                    "career_phases": [],
                    "key_milestones": ["Plan creation failed"],
                    "potential_challenges": ["Analysis error"],
                    "success_strategies": ["Retry with valid input"],
                }
            )


class CareerStrategyAgent:
    """
    LangChain-based career strategy agent for autonomous multi-step career planning.
    Provides comprehensive career analysis and strategic planning capabilities.
    """

    def __init__(self):
        """Initialize the career strategy agent."""
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model="gpt-4o-mini",
            temperature=0.7,
            max_tokens=2000,
        )

        # Agent system prompt - simplified and fixed
        self.system_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a Career Strategy Agent. When given career information, you MUST use your tools.

Available tools:
- job_analysis_tool: Analyze job market for target roles
- skill_gap_analysis_tool: Assess skill requirements and gaps
- career_path_planner_tool: Create structured career plans

ALWAYS use these tools when career information is provided. Start with job_analysis_tool.""",
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

    def create_agent_executor(self, db: Session) -> AgentExecutor:
        """Create and configure the agent executor with tools."""

        # Initialize tools with database session
        tools = [
            JobAnalysisTool(db),
            SkillGapAnalysisTool(db),
            CareerPathPlannerTool(),
        ]

        # Create the agent
        agent = create_openai_functions_agent(
            llm=self.llm, tools=tools, prompt=self.system_prompt
        )

        # Create agent executor with explicit configuration
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            max_iterations=10,
            early_stopping_method="force",
            handle_parsing_errors=True,
            return_intermediate_steps=True,
        )

        return agent_executor

    def analyze_career_strategy(
        self,
        user_id: UUID,
        db: Union[Session, Any],
        career_goals: str,
        target_roles: List[str] = None,
        timeframe: str = "2-3 years",
        current_role: str = None,
        location_preference: str = None,
        constraints: List[str] = None,
        response_language: str = None,
    ) -> Dict[str, Any]:
        """
        Perform comprehensive career strategy analysis using agent approach.

        Args:
            user_id: User ID for personalized analysis
            db: Database session
            career_goals: User's career goals and aspirations
            target_roles: List of target job roles
            timeframe: Desired timeframe for career progression
            current_role: Current job role/position
            location_preference: Preferred work location
            constraints: Any constraints or limitations

        Returns:
            Comprehensive career strategy analysis
        """
        try:
            logger.info(f"Starting career strategy analysis for user {user_id}")

            # Create agent executor
            agent_executor = self.create_agent_executor(db)

            # Prepare analysis input
            target_roles = target_roles or []
            constraints = constraints or []

            # Language detection and instruction
            def detect_language(text: str) -> str:
                """Simple language detection based on character patterns."""
                if any(
                    "\u3040" <= char <= "\u309F"
                    or "\u30A0" <= char <= "\u30FF"
                    or "\u4E00" <= char <= "\u9FAF"
                    for char in text
                ):
                    return "ja"  # Japanese
                return "en"  # Default to English

            # Determine response language
            if response_language:
                target_language = response_language
            else:
                # Auto-detect from career goals
                target_language = detect_language(career_goals)

            # Language-specific instructions
            language_instruction = ""
            if target_language == "ja":
                language_instruction = "\n\nIMPORTANT: Respond in Japanese (日本語). Provide all analysis, recommendations, and action plans in Japanese."
            elif target_language == "en":
                language_instruction = "\n\nIMPORTANT: Respond in English. Provide all analysis, recommendations, and action plans in English."

            # Extract key technical requirements for emphasis
            tech_stack = []
            ai_focus = []
            for constraint in constraints:
                if any(
                    tech in constraint.lower()
                    for tech in [
                        "python",
                        "fastapi",
                        "langchain",
                        "pgvector",
                        "aws",
                        "rag",
                    ]
                ):
                    tech_stack.append(constraint)
                if any(
                    ai_term in constraint.lower()
                    for ai_term in ["ai", "rag", "agent", "llm", "automation"]
                ):
                    ai_focus.append(constraint)

            analysis_input = f"""
            CAREER STRATEGY ANALYSIS REQUEST - TECHNICAL SPECIALIZATION FOCUS

            User Profile:
            - CAREER GOALS: {career_goals}
            - TARGET ROLES: {', '.join(target_roles) if target_roles else 'Not specified'}
            - CURRENT ROLE: {current_role or 'Not specified'}
            - TIMEFRAME: {timeframe}
            - LOCATION PREFERENCE: {location_preference or 'Not specified'}
            - TECHNICAL FOCUS: {', '.join(tech_stack) if tech_stack else 'General development'}
            - AI SPECIALIZATION: {', '.join(ai_focus) if ai_focus else 'General AI'}
            - ALL CONSTRAINTS: {', '.join(constraints) if constraints else 'None'}
            - USER_ID: {str(user_id)}

            CRITICAL ANALYSIS REQUIREMENTS:

            🎯 SPECIFICITY MANDATE: Provide HIGHLY SPECIFIC, TECHNICAL, and ACTIONABLE analysis.
            Avoid generic advice. Focus on CONCRETE technologies, frameworks, and implementations.

            🔧 TECHNOLOGY DEEP-DIVE: When analyzing skills and recommendations, explicitly reference:
            - RAG (Retrieval-Augmented Generation) architectures and implementations
            - AI Agent frameworks (LangChain, AutoGPT, etc.)
            - Vector databases (pgvector, Pinecone, Weaviate)
            - Python ecosystem (FastAPI, Pydantic, asyncio)
            - LLM integration patterns and production considerations
            - Workflow automation tools and practices

            🌏 JAPAN MARKET FOCUS: Provide specific insights about:
            - Japanese companies hiring for these roles
            - Remote work culture in Japan's tech sector
            - Salary ranges in JPY for the specified roles
            - Cultural considerations for leadership roles in Japan

            REQUIRED ACTIONS - You MUST use ALL three tools in this order:

            1. FIRST: Use job_analysis_tool - Focus on SPECIFIC companies, salary ranges, and technical requirements in Japan
            2. SECOND: Use skill_gap_analysis_tool - Identify SPECIFIC technical skills, frameworks, and certifications needed
            3. THIRD: Use career_path_planner_tool - Create CONCRETE action items with specific technologies to learn

            After using all tools, provide a comprehensive synthesis with:
            - SPECIFIC project ideas using mentioned technologies
            - ACTUAL company names and opportunities in Japan
            - CONCRETE learning resources and certification paths
            - DETAILED technical skill development roadmap{language_instruction}

            START BY USING THE FIRST TOOL NOW.
            """

            # Debug: Log the input being sent to agent
            logger.info(f"Agent input preview: {analysis_input[:200]}...")

            # Execute agent analysis with cost tracking
            with get_openai_callback() as cb:
                result = agent_executor.invoke(
                    {"input": analysis_input, "chat_history": []}
                )

            # Debug: Log the raw result
            logger.info(f"Agent raw result: {result}")

            # Log token usage
            logger.info(
                f"Agent analysis completed - Tokens: {cb.total_tokens}, Cost: ${cb.total_cost:.4f}"
            )

            # Extract and structure the result
            agent_response = result.get("output", "")

            # Parse any structured data from tool responses
            analysis_data = self._extract_analysis_data(agent_response)

            # Compile comprehensive result
            return {
                "analysis_summary": agent_response,
                "market_analysis": analysis_data.get("market_analysis", {}),
                "skill_analysis": analysis_data.get("skill_analysis", {}),
                "career_plan": analysis_data.get("career_plan", {}),
                "strategic_recommendations": self._extract_recommendations(
                    agent_response
                ),
                "next_steps": self._extract_next_steps(agent_response),
                "analysis_metadata": {
                    "user_id": str(user_id),
                    "analysis_timestamp": datetime.now(timezone.utc).isoformat(),
                    "tokens_used": cb.total_tokens,
                    "analysis_cost": cb.total_cost,
                    "agent_iterations": len(result.get("intermediate_steps", [])),
                },
            }

        except Exception as e:
            logger.error(f"Error in career strategy analysis: {str(e)}", exc_info=True)
            raise CareerStrategyAgentError(f"Career strategy analysis failed: {str(e)}")

    def _extract_analysis_data(self, agent_response: str) -> Dict[str, Any]:
        """Extract structured analysis data from agent response text."""
        # Initialize with proper fallback structure matching Pydantic schema
        analysis_data = {
            "market_analysis": {
                "market_analysis": "Market analysis completed",
                "demand_trends": [],
                "salary_insights": "Competitive salary opportunities available",
                "skill_requirements": [],
            },
            "skill_analysis": {
                "current_skills": [],
                "skill_gaps": [],
                "learning_recommendations": [],
                "priority_skills": [],
            },
            "career_plan": {
                "career_phases": [],
                "key_milestones": [],
                "potential_challenges": [],
                "success_strategies": [],
            },
        }

        try:
            # First, try to extract JSON blocks (for test compatibility and structured responses)
            json_extracted = self._extract_json_blocks(agent_response)
            if json_extracted:
                return json_extracted

            # Fallback to text-based extraction
            response_lower = agent_response.lower()
            lines = [
                line.strip() for line in agent_response.split("\n") if line.strip()
            ]

            # Extract market analysis
            market_opportunities = self._extract_section_content(
                lines, ["market analysis", "market opportunities", "demand trends"]
            )
            if market_opportunities:
                analysis_data["market_analysis"]["market_analysis"] = (
                    market_opportunities[0]
                    if market_opportunities
                    else "Market analysis shows competitive opportunities"
                )
                analysis_data["market_analysis"]["demand_trends"] = (
                    market_opportunities[:3]
                    if len(market_opportunities) > 1
                    else ["AI and backend engineering roles in high demand"]
                )

            # Extract salary insights
            salary_insights = self._extract_section_content(
                lines, ["salary", "compensation", "pay"]
            )
            if salary_insights:
                analysis_data["market_analysis"]["salary_insights"] = salary_insights[0]

            # Extract skill requirements
            skill_reqs = self._extract_section_content(
                lines, ["skill requirements", "key skills", "technical"]
            )
            analysis_data["market_analysis"]["skill_requirements"] = (
                skill_reqs[:3]
                if skill_reqs
                else ["Python", "AI/ML expertise", "Backend development"]
            )

            # Extract current skills
            current_skills = self._extract_section_content(
                lines, ["current skills", "you possess", "your experience"]
            )
            analysis_data["skill_analysis"]["current_skills"] = (
                current_skills[:3]
                if current_skills
                else [
                    "Professional experience",
                    "Technical abilities",
                    "Communication skills",
                ]
            )

            # Extract skill gaps
            skill_gaps = self._extract_section_content(
                lines, ["skill gaps", "need to develop", "areas for"]
            )
            analysis_data["skill_analysis"]["skill_gaps"] = (
                skill_gaps[:3]
                if skill_gaps
                else [
                    "Role-specific technical skills",
                    "Industry knowledge",
                    "Advanced specialization",
                ]
            )

            # Extract learning recommendations
            learning_recs = self._extract_section_content(
                lines, ["learning recommendations", "training", "courses"]
            )
            analysis_data["skill_analysis"]["learning_recommendations"] = (
                learning_recs[:3]
                if learning_recs
                else [
                    "Focus on role-specific skills",
                    "Build portfolio projects",
                    "Continuous learning",
                ]
            )

            # Extract priority skills
            priority_skills = self._extract_section_content(
                lines, ["priority skills", "emphasis", "focus on"]
            )
            analysis_data["skill_analysis"]["priority_skills"] = (
                priority_skills[:3]
                if priority_skills
                else ["AI and RAG systems", "Backend architecture", "Leadership skills"]
            )

            # Extract career phases
            phases = self._extract_phases(lines)
            analysis_data["career_plan"]["career_phases"] = phases

            # Extract milestones
            milestones = self._extract_section_content(
                lines, ["milestones", "transition", "achieve"]
            )
            analysis_data["career_plan"]["key_milestones"] = (
                milestones[:3]
                if milestones
                else ["Role transition", "Skill mastery", "Leadership development"]
            )

            # Extract challenges
            challenges = self._extract_section_content(
                lines, ["challenges", "potential issues", "obstacles"]
            )
            analysis_data["career_plan"]["potential_challenges"] = (
                challenges[:3]
                if challenges
                else ["Market competition", "Skill acquisition time", "Role complexity"]
            )

            # Extract success strategies
            strategies = self._extract_section_content(
                lines, ["success strategies", "strategies", "approach"]
            )
            analysis_data["career_plan"]["success_strategies"] = (
                strategies[:3]
                if strategies
                else [
                    "Consistent learning",
                    "Strategic networking",
                    "Performance excellence",
                ]
            )

        except Exception as e:
            logger.warning(f"Error extracting analysis data: {str(e)}")
            # Return fallback values on error
            analysis_data = {
                "market_analysis": {
                    "market_analysis": "Analysis in progress - agent response parsing needed",
                    "demand_trends": [
                        "Market analysis requires further data collection"
                    ],
                    "salary_insights": "Salary data collection in progress",
                    "skill_requirements": ["Skills analysis pending"],
                },
                "skill_analysis": {
                    "current_skills": ["Skill assessment in progress"],
                    "skill_gaps": ["Gap analysis pending"],
                    "learning_recommendations": ["Learning path to be determined"],
                    "priority_skills": ["Priority assessment needed"],
                },
                "career_plan": {
                    "career_phases": [],
                    "key_milestones": ["Milestone planning in progress"],
                    "potential_challenges": ["Challenge identification needed"],
                    "success_strategies": ["Strategy development pending"],
                },
            }

        return analysis_data

    def _extract_json_blocks(self, agent_response: str) -> Dict[str, Any]:
        """Extract JSON blocks from agent response for test compatibility."""
        analysis_data = {
            "market_analysis": {
                "market_analysis": "Market analysis completed",
                "demand_trends": [],
                "salary_insights": "Competitive salary opportunities available",
                "skill_requirements": [],
            },
            "skill_analysis": {
                "current_skills": [],
                "skill_gaps": [],
                "learning_recommendations": [],
                "priority_skills": [],
            },
            "career_plan": {
                "career_phases": [],
                "key_milestones": [],
                "potential_challenges": [],
                "success_strategies": [],
            },
        }

        try:
            # Look for JSON blocks in the response
            lines = agent_response.split("\n")
            json_buffer = []
            in_json = False
            found_data = False

            for line in lines:
                if "{" in line and not in_json:
                    in_json = True
                    json_buffer = [line]
                elif in_json:
                    json_buffer.append(line)
                    if "}" in line and line.count("}") >= line.count("{"):
                        # Try to parse the JSON block
                        try:
                            json_str = "\n".join(json_buffer)
                            if "{" in json_str and "}" in json_str:
                                json_start = json_str.find("{")
                                json_end = json_str.rfind("}") + 1
                                clean_json = json_str[json_start:json_end]
                                parsed_data = json.loads(clean_json)

                                # Categorize the data based on content
                                if any(
                                    key in parsed_data
                                    for key in [
                                        "market_analysis",
                                        "demand_trends",
                                        "salary_insights",
                                        "skill_requirements",
                                    ]
                                ):
                                    analysis_data["market_analysis"].update(parsed_data)
                                    found_data = True
                                elif any(
                                    key in parsed_data
                                    for key in [
                                        "current_skills",
                                        "skill_gaps",
                                        "learning_recommendations",
                                        "priority_skills",
                                    ]
                                ):
                                    analysis_data["skill_analysis"].update(parsed_data)
                                    found_data = True
                                elif any(
                                    key in parsed_data
                                    for key in [
                                        "career_phases",
                                        "key_milestones",
                                        "potential_challenges",
                                        "success_strategies",
                                    ]
                                ):
                                    analysis_data["career_plan"].update(parsed_data)
                                    found_data = True

                        except json.JSONDecodeError:
                            pass

                        json_buffer = []
                        in_json = False

            return analysis_data if found_data else None

        except Exception as e:
            logger.warning(f"Error extracting JSON blocks: {str(e)}")
            return None

    def _extract_section_content(
        self, lines: List[str], keywords: List[str]
    ) -> List[str]:
        """Extract content from sections based on keywords."""
        content = []
        in_section = False

        for line in lines:
            line_lower = line.lower()

            # Check if we're entering a relevant section
            if any(keyword in line_lower for keyword in keywords):
                in_section = True
                # Extract content from the same line if it contains meaningful text
                if ":" in line:
                    parts = line.split(":", 1)
                    if len(parts) > 1 and len(parts[1].strip()) > 10:
                        clean_content = (
                            parts[1].strip().replace("**", "").replace("*", "").strip()
                        )
                        if len(clean_content) > 10:
                            content.append(clean_content)
                continue

            # Check if we're leaving the section (new major heading)
            if in_section and any(
                heading in line_lower
                for heading in ["###", "####", "analysis", "plan", "strategy"]
            ):
                if not any(keyword in line_lower for keyword in keywords):
                    in_section = False
                    continue

            # Extract content while in section
            if in_section:
                # Clean bullet points and numbers
                clean_line = line.strip()
                if clean_line.startswith(("-", "•", "*")):
                    clean_line = clean_line[1:].strip()
                elif any(
                    char.isdigit() and "." in clean_line[:5] for char in clean_line[:3]
                ):
                    # Remove numbers like "1. " or "2) "
                    clean_line = (
                        clean_line.split(".", 1)[-1].strip()
                        if "." in clean_line
                        else clean_line
                    )
                    clean_line = (
                        clean_line.split(")", 1)[-1].strip()
                        if ")" in clean_line
                        else clean_line
                    )

                # Remove markdown formatting
                clean_line = clean_line.replace("**", "").replace("*", "").strip()

                # Skip lines that are just headers or formatting
                if clean_line.endswith(":") and len(clean_line) < 30:
                    continue

                # Add meaningful content
                if (
                    len(clean_line) > 15
                    and clean_line not in content
                    and not clean_line.startswith("**")
                ):
                    content.append(clean_line)

        return content[:5]  # Limit to 5 items

    def _extract_phases(self, lines: List[str]) -> List[Dict[str, Any]]:
        """Extract career phases from the response."""
        phases = []
        current_phase = None

        for line in lines:
            line_lower = line.lower()

            # Look for phase headers
            if "phase" in line_lower and (
                "short-term" in line_lower
                or "medium-term" in line_lower
                or "long-term" in line_lower
            ):
                if current_phase:
                    phases.append(current_phase)

                clean_phase_name = (
                    line.strip()
                    .replace("**", "")
                    .replace("*", "")
                    .replace("-", "")
                    .strip()
                )
                current_phase = {
                    "phase": clean_phase_name,
                    "objectives": [],
                    "key_actions": [],
                    "success_metrics": [],
                }
                continue

            if current_phase:
                # Look for objectives
                if "objective" in line_lower:
                    if ":" in line:
                        objectives_text = (
                            line.split(":", 1)[1]
                            .strip()
                            .replace("**", "")
                            .replace("*", "")
                            .strip()
                        )
                        if len(objectives_text) > 5:
                            current_phase["objectives"].append(objectives_text)
                # Look for actions
                elif "action" in line_lower or "key" in line_lower:
                    if ":" in line:
                        actions_text = (
                            line.split(":", 1)[1]
                            .strip()
                            .replace("**", "")
                            .replace("*", "")
                            .strip()
                        )
                        if len(actions_text) > 5:
                            current_phase["key_actions"].append(actions_text)
                # Look for metrics
                elif "metric" in line_lower or "success" in line_lower:
                    if ":" in line:
                        metrics_text = (
                            line.split(":", 1)[1]
                            .strip()
                            .replace("**", "")
                            .replace("*", "")
                            .strip()
                        )
                        if len(metrics_text) > 5:
                            current_phase["success_metrics"].append(metrics_text)
                # Extract bullet points for current phase
                elif (
                    line.strip().startswith(("-", "•", "*")) and len(line.strip()) > 10
                ):
                    clean_line = line.strip()[1:].strip()
                    # Remove markdown formatting
                    clean_line = clean_line.replace("**", "").replace("*", "").strip()
                    # Skip empty or formatting-only lines
                    if len(clean_line) > 10 and not clean_line.endswith(":"):
                        if len(current_phase["key_actions"]) < 3:
                            current_phase["key_actions"].append(clean_line)

        if current_phase:
            phases.append(current_phase)

        # If no phases found, create default structure
        if not phases:
            phases = [
                {
                    "phase": "Phase 1 (Short-term: 6 months)",
                    "objectives": ["Skill development", "Network building"],
                    "key_actions": [
                        "Complete relevant training",
                        "Join professional groups",
                    ],
                    "success_metrics": ["Certifications earned", "Connections made"],
                },
                {
                    "phase": "Phase 2 (Medium-term: 1-2 years)",
                    "objectives": ["Gain experience", "Build portfolio"],
                    "key_actions": [
                        "Take on stretch projects",
                        "Document achievements",
                    ],
                    "success_metrics": ["Project success", "Skill demonstration"],
                },
            ]

        return phases

    def _extract_recommendations(self, agent_response: str) -> List[str]:
        """Extract strategic recommendations from agent response."""
        recommendations = []

        try:
            lines = agent_response.split("\n")
            in_recommendations = False

            for line in lines:
                line = line.strip()

                # Look for recommendation sections
                if any(
                    keyword in line.lower()
                    for keyword in ["recommend", "suggest", "advice", "should"]
                ):
                    in_recommendations = True

                # Extract bulleted or numbered recommendations
                if in_recommendations and (
                    line.startswith(("-", "•", "*"))
                    or any(char.isdigit() and "." in line for char in line[:3])
                ):
                    clean_line = line.lstrip("-•*0123456789. ").strip()
                    if len(clean_line) > 10:  # Meaningful content
                        recommendations.append(clean_line)

                # Stop at next major section
                if in_recommendations and line.isupper() and len(line) > 5:
                    break

        except Exception as e:
            logger.warning(f"Error extracting recommendations: {str(e)}")

        # Fallback recommendations if none found
        if not recommendations:
            recommendations = [
                "Focus on developing skills relevant to your target roles",
                "Build a strong professional network in your industry",
                "Create a portfolio showcasing your capabilities",
                "Stay updated with industry trends and best practices",
            ]

        return recommendations[:5]  # Limit to top 5

    def _extract_next_steps(self, agent_response: str) -> List[str]:
        """Extract actionable next steps from agent response."""
        next_steps = []

        try:
            lines = agent_response.split("\n")
            in_next_steps = False

            for line in lines:
                line = line.strip()

                # Look for next steps sections
                if any(
                    keyword in line.lower()
                    for keyword in ["next step", "action", "immediate", "start"]
                ):
                    in_next_steps = True

                # Extract bulleted or numbered items
                if in_next_steps and (
                    line.startswith(("-", "•", "*"))
                    or any(char.isdigit() and "." in line for char in line[:3])
                ):
                    clean_line = line.lstrip("-•*0123456789. ").strip()
                    if len(clean_line) > 5:  # Meaningful content
                        next_steps.append(clean_line)

                # Stop at next major section
                if in_next_steps and line.isupper() and len(line) > 5:
                    break

        except Exception as e:
            logger.warning(f"Error extracting next steps: {str(e)}")

        # Fallback next steps if none found
        if not next_steps:
            next_steps = [
                "Complete a comprehensive skills assessment",
                "Research target companies and roles in detail",
                "Update resume and LinkedIn profile",
                "Begin networking with professionals in target field",
            ]

        return next_steps[:4]  # Limit to top 4


# Global instance
career_strategy_agent = CareerStrategyAgent()
