from pathlib import Path
import sys

from fastapi.testclient import TestClient

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

import app.main as main_module


client = TestClient(main_module.app)


def test_convert_html_returns_html_text(monkeypatch):
    def fake_build_full_html_document(markdown_text: str, font_css: str = "") -> str:
        assert markdown_text == "# Hello"
        assert font_css == ""
        return "<html><body><h1>Hello</h1></body></html>"

    monkeypatch.setattr(main_module, "build_full_html_document", fake_build_full_html_document)

    response = client.post("/api/convert/html", json={"markdown": "# Hello"})

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "<h1>Hello</h1>" in response.text


def test_convert_pdf_returns_attachment(monkeypatch):
    monkeypatch.setattr(main_module, "resolve_pdf_font_css", lambda: "body{font-family:CustomCJK;}")
    monkeypatch.setattr(main_module, "build_full_html_document", lambda markdown_text, font_css="": "<html><body>PDF</body></html>")
    monkeypatch.setattr(main_module, "export_pdf_bytes", lambda html_text: b"%PDF-1.4")

    response = client.post("/api/convert/pdf", json={"markdown": "# PDF"})

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/octet-stream")
    assert response.headers["content-disposition"] == 'attachment; filename="document.pdf"'
    assert response.content == b"%PDF-1.4"


def test_convert_word_returns_attachment(monkeypatch):
    monkeypatch.setattr(main_module, "export_word_from_markdown", lambda markdown_text: b"DOCX")

    response = client.post("/api/convert/word", json={"markdown": "# Word"})

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/octet-stream")
    assert response.headers["content-disposition"] == 'attachment; filename="document.docx"'
    assert response.content == b"DOCX"


def test_convert_html_rejects_empty_markdown():
    response = client.post("/api/convert/html", json={"markdown": "   "})

    assert response.status_code == 400
    assert response.json()["detail"] == "markdown must not be empty"
