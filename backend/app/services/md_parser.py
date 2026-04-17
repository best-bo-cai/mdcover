from jinja2 import Environment, FileSystemLoader, select_autoescape
import markdown

from app.core.config import TEMPLATE_DIR


env = Environment(
    loader=FileSystemLoader(str(TEMPLATE_DIR)),
    autoescape=select_autoescape(["html", "xml"]),
)


def markdown_to_html_fragment(md_text: str) -> str:
    return markdown.markdown(
        md_text,
        extensions=[
            "fenced_code",
            "tables",
            "nl2br",
            "codehilite",
            "pymdownx.superfences",
            "pymdownx.highlight",
        ],
        extension_configs={
            "codehilite": {
                "guess_lang": False,
                "noclasses": False,
            },
            "pymdownx.highlight": {
                "use_pygments": True,
                "noclasses": False,
            },
        },
    )


def render_full_html(content_html: str, font_family_css: str = "") -> str:
    template = env.get_template("base.html")
    return template.render(content_html=content_html, font_family_css=font_family_css)


def build_full_html_document(md_text: str, font_css: str = "") -> str:
    content_html = markdown_to_html_fragment(md_text)
    return render_full_html(content_html, font_css)
