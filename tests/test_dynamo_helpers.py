# tests for db.dynamo_helpers
import os
import sys
from pathlib import Path
from unittest.mock import patch

_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))


def test_get_pages_returns_none_when_dynamo_unavailable():
    with patch.dict(os.environ, {}, clear=False):
        for k in list(os.environ):
            if k.startswith("AWS_") or k.startswith("DYNAMODB_"):
                del os.environ[k]
        from db import dynamo_helpers
        assert dynamo_helpers.get_pages("https://example.com/topic") is None


def test_get_contents_returns_none_when_dynamo_unavailable():
    with patch.dict(os.environ, {}, clear=False):
        for k in list(os.environ):
            if k.startswith("AWS_") or k.startswith("DYNAMODB_"):
                del os.environ[k]
        from db import dynamo_helpers
        assert dynamo_helpers.get_contents("https://example.com/page") is None


def test_get_article_returns_none_when_dynamo_unavailable():
    with patch.dict(os.environ, {}, clear=False):
        for k in list(os.environ):
            if k.startswith("AWS_") or k.startswith("DYNAMODB_"):
                del os.environ[k]
        from db import dynamo_helpers
        assert dynamo_helpers.get_article("https://example.com/article") is None
