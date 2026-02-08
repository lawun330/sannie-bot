# tests for telegram-bot handlers
import importlib.util
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# add telegram-bot dir so "app" and "credentials" can be loaded from there
_root = Path(__file__).resolve().parent.parent
_bot_dir = _root / "telegram-bot"
if str(_bot_dir) not in sys.path:
    sys.path.insert(0, str(_bot_dir))


@pytest.mark.asyncio
async def test_help_function_replies_with_bbc_or_news():
    """help_function should call reply_text once with text containing 'BBC' or 'news'."""
    # mock credentials before loading app so BOT_TOKEN/BOT_USERNAME are not required
    creds = MagicMock()
    creds.BOT_TOKEN = "fake"
    creds.BOT_USERNAME = "fake"
    with patch.dict(sys.modules, {"credentials": creds}):
        spec = importlib.util.spec_from_file_location("app", _bot_dir / "app.py")
        app_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(app_mod)
    update = MagicMock()
    update.message.reply_text = AsyncMock()
    context = MagicMock()
    await app_mod.help_function(update, context)
    update.message.reply_text.assert_called_once()
    text = update.message.reply_text.call_args[0][0]
    assert "BBC" in text or "news" in text.lower()
