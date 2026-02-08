# tests for FastAPI endpoints (api.py):
# - set chosen topic/page/content,
# - get chosen topic/page/content,
# - pages/contents/article
from fastapi.testclient import TestClient


def test_set_chosen_topic_missing_body(api_client: TestClient):
    """POST /set_chosen_topic with no topic in body should return 200 with error or message key."""
    r = api_client.post("/set_chosen_topic", json={})
    assert r.status_code == 200
    assert "error" in r.json() or "message" in r.json()


def test_set_chosen_topic_success(api_client_and_mocks):
    """POST /set_chosen_topic with valid topic link should succeed and call redis setex."""
    client, mock_redis, *_ = api_client_and_mocks
    r = client.post("/set_chosen_topic", json={"topic": "https://example.com/topic"})
    assert r.status_code == 200
    assert r.json().get("message") == "Topic set successfully"
    mock_redis.setex.assert_called_once()


def test_set_chosen_page_success(api_client_and_mocks):
    """POST /set_chosen_page with valid page link should succeed and call redis setex."""
    client, mock_redis, *_ = api_client_and_mocks
    r = client.post("/set_chosen_page", json={"page": "https://example.com/page"})
    assert r.status_code == 200
    assert r.json().get("message") == "Page set successfully"
    mock_redis.setex.assert_called_once()


def test_set_chosen_content_success(api_client_and_mocks):
    """POST /set_chosen_content with valid content link should succeed and call redis setex."""
    client, mock_redis, *_ = api_client_and_mocks
    r = client.post("/set_chosen_content", json={"content": "https://example.com/article"})
    assert r.status_code == 200
    assert r.json().get("message") == "Content/article set successfully"
    mock_redis.setex.assert_called_once()


def test_get_chosen_topic_page_content(api_client: TestClient):
    """GET /get_chosen_topic, /get_chosen_page, /get_chosen_content should return 200 (cache or null)."""
    for path in ["/get_chosen_topic", "/get_chosen_page", "/get_chosen_content"]:
        r = api_client.get(path)
        assert r.status_code == 200


def test_pages_requires_chosen_topic(api_client: TestClient):
    """GET /pages without a chosen topic in redis should return 400."""
    r = api_client.get("/pages")
    assert r.status_code == 400


def test_pages_returns_from_scraper_when_redis_and_dynamo_miss(api_client_and_mocks):
    """GET /pages with chosen_topic set but no cache/DB hit should return mocked scraper page list."""
    client, mock_redis, mock_dynamo, fetch_pages, *_ = api_client_and_mocks
    mock_redis.get.side_effect = lambda k: "https://example.com/topic" if k == "chosen_topic" else None
    mock_dynamo.get_pages.return_value = None
    fetch_pages.return_value = ["https://example.com/page1", "https://example.com/page2"]
    r = client.get("/pages")
    assert r.status_code == 200
    assert r.json() == ["https://example.com/page1", "https://example.com/page2"]


def test_contents_requires_chosen_page(api_client: TestClient):
    """GET /contents without a chosen page in redis should return 400."""
    r = api_client.get("/contents")
    assert r.status_code == 400


def test_contents_returns_from_scraper_when_miss(api_client_and_mocks):
    """GET /contents with chosen_page set but no cache/DB hit should return mocked content links."""
    client, mock_redis, mock_dynamo, _, fetch_content_links, _ = api_client_and_mocks
    mock_redis.get.side_effect = lambda k: "https://example.com/page" if k == "chosen_page" else None
    mock_dynamo.get_contents.return_value = None
    fetch_content_links.return_value = [{"url": "https://a.com/1", "header": "H1"}]
    r = client.get("/contents")
    assert r.status_code == 200
    assert r.json() == [{"url": "https://a.com/1", "header": "H1"}]


def test_article_requires_chosen_content(api_client: TestClient):
    """GET /article without a chosen content in redis should return 400."""
    r = api_client.get("/article")
    assert r.status_code == 400


def test_article_returns_from_scraper_when_miss(api_client_and_mocks):
    """GET /article with chosen_content set but no cache/DB hit should return mocked article text."""
    client, mock_redis, mock_dynamo, _, _, get_article = api_client_and_mocks
    mock_redis.get.side_effect = lambda k: "https://example.com/article" if k == "chosen_content" else None
    mock_dynamo.get_article.return_value = None
    get_article.return_value = "Fake article text"
    r = client.get("/article")
    assert r.status_code == 200
    assert r.json() == "Fake article text"
