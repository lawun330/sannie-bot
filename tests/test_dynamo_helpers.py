# tests for db.dynamo_helpers:
# - get_pages,
# - get_contents,
# - get_article when DynamoDB is not configured
import os
import sys
from pathlib import Path
from unittest.mock import patch

# ensure project root is on path so "db" package resolves
_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))


def test_get_pages_returns_none_when_dynamo_unavailable():
    """when AWS/DynamoDB env vars are unset, get_pages should return None (no real DB)."""
    with patch.dict(os.environ, {}, clear=False):
        for k in list(os.environ):
            if k.startswith("AWS_") or k.startswith("DYNAMODB_"):
                del os.environ[k]
        from db import dynamo_helpers
        assert dynamo_helpers.get_pages("https://example.com/topic") is None


def test_get_contents_returns_none_when_dynamo_unavailable():
    """when AWS/DynamoDB env vars are unset, get_contents should return None (no real DB)."""
    with patch.dict(os.environ, {}, clear=False):
        for k in list(os.environ):
            if k.startswith("AWS_") or k.startswith("DYNAMODB_"):
                del os.environ[k]
        from db import dynamo_helpers
        assert dynamo_helpers.get_contents("https://example.com/page") is None


def test_get_article_returns_none_when_dynamo_unavailable():
    """when AWS/DynamoDB env vars are unset, get_article should return None (no real DB)."""
    with patch.dict(os.environ, {}, clear=False):
        for k in list(os.environ):
            if k.startswith("AWS_") or k.startswith("DYNAMODB_"):
                del os.environ[k]
        from db import dynamo_helpers
        assert dynamo_helpers.get_article("https://example.com/article") is None
