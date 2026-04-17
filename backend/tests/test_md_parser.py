from pathlib import Path
import sys

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.services.md_parser import markdown_to_html_fragment


def test_markdown_bold_line_keeps_newline_as_html_break():
    html = markdown_to_html_fragment("**bold line**\nnext line")

    assert "<strong>bold line</strong><br" in html
