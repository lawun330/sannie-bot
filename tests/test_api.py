# tests for FastAPI endpoints (api.py)
from fastapi.testclient import TestClient


def test_set_chosen_topic_missing_body(api_client: TestClient):
    r = api_client.post("/set_chosen_topic", json={})
    assert r.status_code == 200
    assert "error" in r.json() or "message" in r.json()


def test_set_chosen_topic_success(api_client_and_mocks):
    client, mock_redis, *_ = api_client_and_mocks
    r = client.post("/set_chosen_topic", json={"topic": "https://example.com/topic"})
    assert r.status_code == 200
    assert r.json().get("message") == "Topic set successfully"
    mock_redis.setex.assert_called_once()


def test_set_chosen_page_success(api_client_and_mocks):
    client, mock_redis, *_ = api_client_and_mocks
    r = client.post("/set_chosen_page", json={"page": "https://example.com/page"})
    assert r.status_code == 200
    assert r.json().get("message") == "Page set successfully"
    mock_redis.setex.assert_called_once()


def test_set_chosen_content_success(api_client_and_mocks):
    client, mock_redis, *_ = api_client_and_mocks
    r = client.post("/set_chosen_content", json={"content": "https://example.com/article"})
    assert r.status_code == 200
    assert r.json().get("message") == "Content/article set successfully"
    mock_redis.setex.assert_called_once()


def test_get_chosen_topic_page_content(api_client: TestClient):
    for path in ["/get_chosen_topic", "/get_chosen_page", "/get_chosen_content"]:
        r = api_client.get(path)
        assert r.status_code == 200


def test_pages_requires_chosen_topic(api_client: TestClient):
    r = api_client.get("/pages")
    assert r.status_code == 400


def test_pages_returns_from_scraper_when_redis_and_dynamo_miss(api_client_and_mocks):
    client, mock_redis, mock_dynamo, fetch_pages, *_ = api_client_and_mocks
    mock_redis.get.side_effect = lambda k: "https://example.com/topic" if k == "chosen_topic" else None
    mock_dynamo.get_pages.return_value = None
    fetch_pages.return_value = ["https://example.com/page1", "https://example.com/page2"]
    r = client.get("/pages")
    assert r.status_code == 200
    assert r.json() == ["https://example.com/page1", "https://example.com/page2"]


def test_contents_requires_chosen_page(api_client: TestClient):
    r = api_client.get("/contents")
    assert r.status_code == 400


def test_contents_returns_from_scraper_when_miss(api_client_and_mocks):
    client, mock_redis, mock_dynamo, _, fetch_content_links, _ = api_client_and_mocks
    mock_redis.get.side_effect = lambda k: "https://example.com/page" if k == "chosen_page" else None
    mock_dynamo.get_contents.return_value = None
    fetch_content_links.return_value = [{"url": "https://a.com/1", "header": "H1"}]
    r = client.get("/contents")
    assert r.status_code == 200
    assert r.json() == [{"url": "https://a.com/1", "header": "H1"}]


def test_article_requires_chosen_content(api_client: TestClient):
    r = api_client.get("/article")
    assert r.status_code == 400


def test_article_returns_from_scraper_when_miss(api_client_and_mocks):
    client, mock_redis, mock_dynamo, _, _, get_article = api_client_and_mocks
    mock_redis.get.side_effect = lambda k: "https://example.com/article" if k == "chosen_content" else None
    mock_dynamo.get_article.return_value = None
    get_article.return_value = "Fake article text"
    r = client.get("/article")
    assert r.status_code == 200
    assert r.json() == "Fake article text"
