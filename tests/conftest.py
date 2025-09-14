from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture(autouse=True)
def mock_embedding_service():
    """Mock embedding service for all tests."""
    with patch("app.services.embedding_service.embedding_service"):
        yield


@pytest.fixture(autouse=True)
def mock_db_session():
    """Mock database session for all tests."""
    mock_session = MagicMock()
    with patch("app.db.session.SessionLocal", return_value=mock_session):
        with patch("app.db.session.get_db") as mock_get_db:
            mock_get_db.return_value = iter([mock_session])
            yield mock_session


@pytest.fixture(autouse=True)
def mock_similarity_service():
    """Mock similarity service for all tests."""
    with patch("app.services.similarity_service.similarity_service"):
        yield


@pytest.fixture(autouse=True)
def mock_openai_client():
    """Mock OpenAI client initialization for all services."""
    import openai

    mock_client = MagicMock()
    with patch.object(openai, "OpenAI", return_value=mock_client):
        yield mock_client


@pytest.fixture(autouse=True)
def mock_langchain_components():
    """Mock LangChain components for career strategy agent."""
    mock_agent = MagicMock()
    mock_executor = MagicMock()
    mock_tools = [MagicMock(name=f"tool_{i}") for i in range(3)]
    mock_tools[0].name = "job_analysis_tool"
    mock_tools[1].name = "skill_gap_analysis_tool"
    mock_tools[2].name = "career_path_planner_tool"
    mock_executor.tools = mock_tools
    mock_executor.agent = mock_agent

    with (
        patch("app.services.career_strategy_agent.ChatOpenAI"),
        patch(
            "app.services.career_strategy_agent.create_openai_functions_agent",
            return_value=mock_agent,
        ),
        patch(
            "app.services.career_strategy_agent.AgentExecutor",
            return_value=mock_executor,
        ),
        patch("app.services.career_strategy_agent.get_openai_callback"),
    ):
        yield


@pytest.fixture(autouse=True)
def mock_openai_api_key():
    """Mock OpenAI API key for all tests."""
    import os

    original_key = os.environ.get("OPENAI_API_KEY")
    os.environ["OPENAI_API_KEY"] = "test-api-key-for-testing"
    yield
    if original_key is not None:
        os.environ["OPENAI_API_KEY"] = original_key
    else:
        os.environ.pop("OPENAI_API_KEY", None)


# Remove the global dependency override to allow testing authentication
@pytest.fixture(autouse=True)
def clear_dependency_overrides():
    """Clear any dependency overrides after each test."""
    yield
    from app.main import app

    app.dependency_overrides.clear()
