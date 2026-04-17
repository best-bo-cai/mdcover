from app.core.config import FONT_PATH
from app.core.exceptions import ConversionError


def resolve_pdf_font_css() -> str:
    if not FONT_PATH.exists():
        raise ConversionError(
            f"PDF font file not found at {FONT_PATH}. Please place a valid OTF/TTF font in backend/fonts/."
        )

    font_uri = FONT_PATH.as_uri()
    return f"""
    @font-face {{
      font-family: 'CustomCJK';
      src: url('{font_uri}') format('opentype');
      font-weight: normal;
      font-style: normal;
    }}

    body {{
      font-family: 'CustomCJK', 'PingFang SC', 'Microsoft YaHei', sans-serif;
    }}
    """


def export_pdf_bytes(html_text: str) -> bytes:
    try:
        from weasyprint import HTML

        return HTML(string=html_text).write_pdf()
    except Exception as exc:
        raise ConversionError(f"failed to render PDF: {exc}") from exc
