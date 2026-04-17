from pathlib import Path
import sys

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.services.word_exporter import export_word_from_markdown


def test_export_word_preserves_single_newline_as_hard_break():
    docx_bytes = export_word_from_markdown("line1\nline2\nline3")
    assert isinstance(docx_bytes, bytes)
    assert len(docx_bytes) > 0

    temp_docx = Path("/tmp/mdcover-linebreak-test.docx")
    temp_docx.write_bytes(docx_bytes)

    import pypandoc

    markdown_roundtrip = pypandoc.convert_file(str(temp_docx), to="markdown", format="docx")

    assert "line1\\line2\\line3" in markdown_roundtrip.replace("\n", "")


def test_export_word_parses_headings_and_lists_in_compact_markdown():
    markdown_text = "intro line\n# H1\n## H2\n- item1\n- item2"
    docx_bytes = export_word_from_markdown(markdown_text)

    temp_docx = Path("/tmp/mdcover-block-syntax-test.docx")
    temp_docx.write_bytes(docx_bytes)

    import pypandoc

    markdown_roundtrip = pypandoc.convert_file(str(temp_docx), to="markdown", format="docx")

    assert "\\# H1" not in markdown_roundtrip
    assert "\\## H2" not in markdown_roundtrip
    assert "# H1" in markdown_roundtrip
    assert "## H2" in markdown_roundtrip
    assert "- item1\\\n" not in markdown_roundtrip
