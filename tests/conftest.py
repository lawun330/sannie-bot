# shared fixtures for testing api, scraper, dynamo, and bot
import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

# ensure project root is on path so "api" and "webscraper" resolve when tests run
_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from api import app as fastapi_app


@pytest.fixture
def mock_redis():
    """patch Redis so tests don't need a real Redis server; get/setex return None by default."""
    with patch("api.redis_client") as m:
        m.get.return_value = None
        m.setex.return_value = None
        yield m


@pytest.fixture
def mock_dynamo():
    """patch DynamoDB helpers so tests don't need AWS; all get/put return None or no-op."""
    with patch("api.dynamo_helpers") as m:
        m.get_pages.return_value = None
        m.get_contents.return_value = None
        m.get_article.return_value = None
        m.put_pages.return_value = None
        m.put_contents.return_value = None
        m.put_article.return_value = None
        yield m


@pytest.fixture
def mock_scraper():
    """patch webscraper fetch functions so tests don't hit the network; return fake data."""
    with patch("api.fetch_pages") as fp, patch("api.fetch_content_links") as fc, patch("api.get_article") as ga:
        fp.return_value = ["https://example.com/page1"]
        fc.return_value = [{"url": "https://example.com/article1", "header": "Test"}]
        ga.return_value = "Sample article content"
        yield fp, fc, ga


@pytest.fixture
def api_client(mock_redis, mock_dynamo, mock_scraper):
    """FastAPI test client with Redis, DynamoDB, and scraper mocked (for simple endpoint tests)."""
    return TestClient(fastapi_app)


@pytest.fixture
def api_client_and_mocks(mock_redis, mock_dynamo, mock_scraper):
    """client plus mocks so tests can set return values (e.g. chosen_topic in redis) per test."""
    client = TestClient(fastapi_app)
    fp, fc, ga = mock_scraper
    return client, mock_redis, mock_dynamo, fp, fc, ga
