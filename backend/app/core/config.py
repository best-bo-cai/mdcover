from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
TEMPLATE_DIR = BASE_DIR / "app" / "templates"
FONT_DIR = BASE_DIR / "fonts"
FONT_FILE_NAME = "SourceHanSansSC-Regular.otf"
FONT_PATH = FONT_DIR / FONT_FILE_NAME

DEFAULT_HTML_FILENAME = "document.html"
DEFAULT_PDF_FILENAME = "document.pdf"
DEFAULT_WORD_FILENAME = "document.docx"
