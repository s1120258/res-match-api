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
def mock_llm_service():
    """Mock LLM service for all tests."""
    with patch("app.services.llm_service.llm_service"):
        yield


@pytest.fixture(autouse=True)
def mock_skill_analysis_service():
    """Mock skill analysis service for all tests."""
    with patch("app.services.skill_analysis_service.skill_analysis_service"):
        yield


@pytest.fixture(autouse=True)
def mock_skill_extraction_service():
    """Mock skill extraction service for all tests."""
    with patch("app.services.skill_extraction_service.skill_extraction_service"):
        yield


@pytest.fixture(autouse=True)
def mock_career_strategy_agent():
    """Mock career strategy agent for all tests."""
    with patch("app.services.career_strategy_agent.CareerStrategyAgent"):
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
