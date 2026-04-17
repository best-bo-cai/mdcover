from pathlib import Path
import tempfile

import pypandoc

from app.core.exceptions import ConversionError


def export_word_from_markdown(md_text: str) -> bytes:
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "document.docx"
            pypandoc.convert_text(
                source=md_text,
                to="docx",
                format="gfm+hard_line_breaks",
                outputfile=str(output_path),
                extra_args=["--highlight-style=tango"],
            )
            return output_path.read_bytes()
    except Exception as exc:
        raise ConversionError(f"failed to render Word document: {exc}") from exc
