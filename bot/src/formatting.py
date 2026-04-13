"""Convert LLM markdown output to Telegram-safe HTML."""

import re
from html import escape


def md_to_tg_html(text: str) -> str:
    """Convert common Markdown to Telegram-compatible HTML.

    Telegram supports: <b>, <i>, <code>, <pre>, <a>, <s>, <u>.
    Does NOT support: headers, lists, horizontal rules as HTML.
    """
    # Escape HTML entities first
    text = escape(text)

    # Code blocks: ```...```
    text = re.sub(r"```(\w*)\n(.*?)```", r"<pre>\2</pre>", text, flags=re.DOTALL)

    # Inline code: `...`
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)

    # Bold: **text** or __text__
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"__(.+?)__", r"<b>\1</b>", text)

    # Italic: *text* or _text_
    text = re.sub(r"\*(.+?)\*", r"<i>\1</i>", text)
    text = re.sub(r"(?<!\w)_(.+?)_(?!\w)", r"<i>\1</i>", text)

    # Strikethrough: ~~text~~
    text = re.sub(r"~~(.+?)~~", r"<s>\1</s>", text)

    # Headers: # text → bold
    text = re.sub(r"^#{1,6}\s+(.+)$", r"<b>\1</b>", text, flags=re.MULTILINE)

    # List items: keep as-is with bullet/dash (Telegram renders plain text fine)
    # Just normalize - and * list markers to •
    text = re.sub(r"^[\-\*]\s+", "• ", text, flags=re.MULTILINE)

    return text
