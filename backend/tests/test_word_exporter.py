from pathlib import Path
import sys

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.services.word_exporter import export_word_from_markdown


def test_export_word_uses_tango_highlight(monkeypatch):
    captured = {}

    def fake_convert_text(*, source, to, format, outputfile, extra_args):
        captured["source"] = source
        captured["to"] = to
        captured["format"] = format
        captured["extra_args"] = extra_args
        Path(outputfile).write_bytes(b"DOCX-BYTES")

    monkeypatch.setattr("app.services.word_exporter.pypandoc.convert_text", fake_convert_text)

    result = export_word_from_markdown("# Title")

    assert result == b"DOCX-BYTES"
    assert captured["source"] == "# Title"
    assert captured["to"] == "docx"
    assert captured["format"] == "gfm+hard_line_breaks"
    assert "--highlight-style=tango" in captured["extra_args"]
