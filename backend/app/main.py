from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import (
    DEFAULT_HTML_FILENAME,
    DEFAULT_PDF_FILENAME,
    DEFAULT_WORD_FILENAME,
)
from app.core.exceptions import ConversionError
from app.models.schema import ConvertRequest
from app.services.md_parser import build_full_html_document
from app.services.pdf_exporter import export_pdf_bytes, resolve_pdf_font_css
from app.services.word_exporter import export_word_from_markdown

app = FastAPI(title="Markdown Converter API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _validate_markdown(markdown_text: str) -> None:
    if not markdown_text.strip():
        raise HTTPException(status_code=400, detail="markdown must not be empty")


@app.exception_handler(ConversionError)
async def conversion_error_handler(_, exc: ConversionError):
    return JSONResponse(status_code=500, content={"detail": exc.message})


@app.get("/api/health")
def health_check():
    return {"status": "ok"}


@app.post("/api/convert/html")
def convert_html(payload: ConvertRequest):
    _validate_markdown(payload.markdown)
    html = build_full_html_document(payload.markdown, font_css="")
    headers = {
        "Content-Disposition": f'attachment; filename="{DEFAULT_HTML_FILENAME}"',
    }
    return Response(content=html, media_type="text/html; charset=utf-8", headers=headers)


@app.post("/api/convert/pdf")
def convert_pdf(payload: ConvertRequest):
    _validate_markdown(payload.markdown)
    font_css = resolve_pdf_font_css()
    html = build_full_html_document(payload.markdown, font_css=font_css)
    pdf_bytes = export_pdf_bytes(html)
    headers = {
        "Content-Disposition": f'attachment; filename="{DEFAULT_PDF_FILENAME}"',
    }
    return Response(
        content=pdf_bytes,
        media_type="application/octet-stream",
        headers=headers,
    )


@app.post("/api/convert/word")
def convert_word(payload: ConvertRequest):
    _validate_markdown(payload.markdown)
    word_bytes = export_word_from_markdown(payload.markdown)
    headers = {
        "Content-Disposition": f'attachment; filename="{DEFAULT_WORD_FILENAME}"',
    }
    return Response(
        content=word_bytes,
        media_type="application/octet-stream",
        headers=headers,
    )
