#!/usr/bin/env python3
"""Render a Smithian Fold Theory Markdown paper as a publication-quality PDF."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    LongTable,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)


NAVY = colors.HexColor("#102A43")
TEAL = colors.HexColor("#087F8C")
CYAN = colors.HexColor("#DDF4F5")
PALE = colors.HexColor("#F3F7FA")
MID = colors.HexColor("#637381")
RULE = colors.HexColor("#C9D6E2")
TEXT = colors.HexColor("#172B4D")


def register_fonts() -> None:
    base = Path("/System/Library/Fonts/Supplemental")
    pdfmetrics.registerFont(TTFont("Ernos", str(base / "Arial Unicode.ttf")))
    pdfmetrics.registerFont(TTFont("ErnosBold", str(base / "Arial Bold.ttf")))
    pdfmetrics.registerFont(TTFont("ErnosItalic", str(base / "Arial Italic.ttf")))
    pdfmetrics.registerFont(TTFont("ErnosBoldItalic", str(base / "Arial Bold Italic.ttf")))
    pdfmetrics.registerFontFamily(
        "Ernos",
        normal="Ernos",
        bold="ErnosBold",
        italic="ErnosItalic",
        boldItalic="ErnosBoldItalic",
    )


def formula_text(value: str) -> str:
    superscript_digits = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺", "0123456789-+")
    value = re.sub(
        r"[⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺]+",
        lambda match: "^(" + match.group(0).translate(superscript_digits) + ")",
        value,
    )
    replacements = {
        r"\operatorname{cast\_out}": "cast_out",
        r"\operatorname{cast_out}": "cast_out",
        r"\Longrightarrow": "⇒",
        r"\longrightarrow": "→",
        r"\rightarrow": "→",
        r"\left": "",
        r"\right": "",
        r"\qquad": "    ",
        r"\quad": "  ",
        r"\cdots": "…",
        r"\cdot": "·",
        r"\times": "×",
        r"\pm": "±",
        r"\alpha": "α",
        r"\varepsilon": "ε",
        r"\hbar": "ℏ",
        r"\pi": "π",
        r"\beta": "β",
        r"\gamma": "γ",
        r"\phi": "φ",
        r"\psi": "ψ",
        r"\sigma": "σ",
        r"\Omega": "Ω",
        r"\lambda": "λ",
        r"\omega": "ω",
        r"\rho": "ρ",
        r"\nu": "ν",
        r"\Delta": "Δ",
        r"\nabla": "∇",
        r"\partial": "∂",
        r"\sum": "Σ",
        r"\max": "max",
        r"\in": "∈",
        r"\le": "≤",
        r"\ge": "≥",
        r"\ne": "≠",
        r"\circ": "°",
        r"\text{Å}": "Å",
        r"\!": "",
        r"\,": " ",
        r"\;": " ",
        r"\lfloor": "⌊",
        r"\rfloor": "⌋",
        r"\mathbb{Q}": "Q",
        r"\ldots": "…",
        r"\_": "_",
    }
    value = value.strip().replace("$", "")
    for old, new in replacements.items():
        value = value.replace(old, new)
    previous = None
    while previous != value:
        previous = value
        value = re.sub(r"_\{([^{}]+)\}", r"_(\1)", value)
        value = re.sub(r"\^\{([^{}]+)\}", r"^(\1)", value)
    value = re.sub(r"\\frac(\d)\{([^{}]+)\}", r"(\1)/(\2)", value)
    value = re.sub(r"\\frac(\d)(\d)", r"\1/\2", value)
    previous = None
    while previous != value:
        previous = value
        value = re.sub(r"\\frac\{([^{}]+)\}\{([^{}]+)\}", r"(\1)/(\2)", value)
    previous = None
    while previous != value:
        previous = value
        value = re.sub(r"\\(?:mathrm|operatorname|boxed)\{([^{}]+)\}", r"\1", value)
    value = value.replace("\\[", "").replace("\\]", "")
    return value


def inline_markup(value: str) -> str:
    code_spans: list[str] = []

    def protect_code(match: re.Match[str]) -> str:
        code_spans.append(match.group(1))
        return f"ERNOSCODETOKEN{len(code_spans) - 1}END"

    value = re.sub(r"`([^`]+)`", protect_code, value.strip())
    value = html.escape(formula_text(value), quote=True)
    value = re.sub(
        r"\[([^\]]+)\]\((https?://[^)]+)\)",
        r'<link href="\2" color="#087F8C"><u>\1</u></link>',
        value,
    )
    value = re.sub(
        r"&lt;(https?://[^&]+)&gt;",
        r'<link href="\1" color="#087F8C"><u>\1</u></link>',
        value,
    )
    value = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", value)
    value = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", value)
    for index, code in enumerate(code_spans):
        rendered = html.escape(formula_text(code), quote=True)
        value = value.replace(
            f"ERNOSCODETOKEN{index}END",
            f'<font name="Ernos">{rendered}</font>',
        )
    return value


def make_styles() -> dict[str, ParagraphStyle]:
    sample = getSampleStyleSheet()
    common = dict(fontName="Ernos", textColor=TEXT, allowWidows=0, allowOrphans=0)
    return {
        "body": ParagraphStyle(
            "Body",
            parent=sample["BodyText"],
            fontSize=9.25,
            leading=13.1,
            spaceAfter=6.2,
            alignment=TA_LEFT,
            **common,
        ),
        "abstract": ParagraphStyle(
            "Abstract",
            parent=sample["BodyText"],
            fontSize=9.5,
            leading=13.8,
            spaceAfter=7,
            leftIndent=7 * mm,
            rightIndent=7 * mm,
            **common,
        ),
        "h1": ParagraphStyle(
            "Part",
            parent=sample["Heading1"],
            fontName="ErnosBold",
            fontSize=17,
            leading=20,
            textColor=NAVY,
            spaceBefore=13,
            spaceAfter=7,
            keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "Section",
            parent=sample["Heading2"],
            fontName="ErnosBold",
            fontSize=13.2,
            leading=16,
            textColor=TEAL,
            spaceBefore=10,
            spaceAfter=5,
            keepWithNext=True,
        ),
        "h3": ParagraphStyle(
            "Subsection",
            parent=sample["Heading3"],
            fontName="ErnosBold",
            fontSize=10.5,
            leading=13.2,
            textColor=NAVY,
            spaceBefore=7,
            spaceAfter=4,
            keepWithNext=True,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            parent=sample["BodyText"],
            fontName="Ernos",
            fontSize=9.1,
            leading=12.7,
            leftIndent=6 * mm,
            firstLineIndent=-3.5 * mm,
            bulletIndent=1.5 * mm,
            spaceAfter=3,
            textColor=TEXT,
        ),
        "quote": ParagraphStyle(
            "Quote",
            parent=sample["BodyText"],
            fontName="ErnosItalic",
            fontSize=9,
            leading=13,
            leftIndent=8 * mm,
            rightIndent=6 * mm,
            borderColor=TEAL,
            borderWidth=1.5,
            borderPadding=(3, 6, 3, 8),
            backColor=PALE,
            textColor=TEXT,
            spaceAfter=7,
        ),
        "formula": ParagraphStyle(
            "Formula",
            parent=sample["BodyText"],
            fontName="Ernos",
            fontSize=10.5,
            leading=14,
            alignment=TA_CENTER,
            textColor=NAVY,
            backColor=PALE,
            borderColor=RULE,
            borderWidth=0.5,
            borderPadding=5,
            spaceBefore=4,
            spaceAfter=8,
        ),
        "code": ParagraphStyle(
            "Code",
            fontName="Courier",
            fontSize=6.7,
            leading=9,
            leftIndent=4 * mm,
            rightIndent=4 * mm,
            backColor=colors.HexColor("#EEF2F6"),
            borderColor=RULE,
            borderWidth=0.5,
            borderPadding=6,
            textColor=colors.HexColor("#243B53"),
            spaceBefore=4,
            spaceAfter=8,
        ),
        "toc": ParagraphStyle(
            "TOC",
            fontName="Ernos",
            fontSize=9.6,
            leading=14.2,
            textColor=TEXT,
            leftIndent=3 * mm,
            spaceAfter=1,
        ),
    }


class PublicationDoc(BaseDocTemplate):
    def __init__(self, filename: str, args: argparse.Namespace):
        self.args = args
        super().__init__(
            filename,
            pagesize=A4,
            leftMargin=20 * mm,
            rightMargin=20 * mm,
            topMargin=20 * mm,
            bottomMargin=18 * mm,
            title=args.title,
            author="Maria Smith - Ernos Labs",
            subject=args.subtitle,
            keywords=args.keywords,
        )
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="body")
        self.addPageTemplates(PageTemplate(id="paper", frames=[frame], onPage=self.decorate))

    def decorate(self, canvas, doc) -> None:
        canvas.saveState()
        page = canvas.getPageNumber()
        width, height = A4
        if page > 1:
            canvas.setStrokeColor(RULE)
            canvas.setLineWidth(0.45)
            canvas.line(20 * mm, height - 13 * mm, width - 20 * mm, height - 13 * mm)
            canvas.setFont("Ernos", 7.2)
            canvas.setFillColor(MID)
            header = self.args.short_title.upper()
            canvas.drawString(20 * mm, height - 10 * mm, header[:105])
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(0.45)
        canvas.line(20 * mm, 12 * mm, width - 20 * mm, 12 * mm)
        canvas.setFillColor(MID)
        canvas.setFont("Ernos", 7.2)
        canvas.drawString(20 * mm, 8 * mm, f"doi:{self.args.doi}")
        canvas.drawRightString(width - 20 * mm, 8 * mm, f"{page}")
        canvas.restoreState()


def cover(args: argparse.Namespace) -> list:
    story = [Spacer(1, 10 * mm)]
    story.append(
        Paragraph(
            "ERNOS LABS&nbsp;&nbsp;&nbsp;·&nbsp;&nbsp;&nbsp;SMITHIAN FOLD THEORY",
            ParagraphStyle("Brand", fontName="ErnosBold", fontSize=9, leading=12, textColor=TEAL, alignment=TA_CENTER, spaceAfter=15),
        )
    )
    story.append(
        Paragraph(
            inline_markup(args.title).replace(" - ", "<br/>"),
            ParagraphStyle("Title", fontName="ErnosBold", fontSize=24, leading=28, textColor=NAVY, alignment=TA_CENTER, spaceAfter=10),
        )
    )
    story.append(
        Paragraph(
            inline_markup(args.subtitle),
            ParagraphStyle("Subtitle", fontName="Ernos", fontSize=13, leading=17, textColor=TEAL, alignment=TA_CENTER, spaceAfter=15),
        )
    )
    story.append(Paragraph("<b>Maria Smith</b><br/>Ernos Labs", ParagraphStyle("Author", fontName="Ernos", fontSize=11, leading=15, textColor=TEXT, alignment=TA_CENTER, spaceAfter=9)))
    edition = html.escape(args.edition)
    if not edition.lower().startswith("publication edition"):
        edition = f"Publication edition {edition}"
    story.append(Paragraph(f'{html.escape(args.date)}&nbsp;&nbsp;·&nbsp;&nbsp;{edition}<br/><link href="https://doi.org/{args.doi}" color="#087F8C"><u>doi:{args.doi}</u></link>', ParagraphStyle("Edition", fontName="Ernos", fontSize=9, leading=13, textColor=MID, alignment=TA_CENTER, spaceAfter=16)))

    box_data = [
        [Paragraph(f"<b>{html.escape(args.result_label.upper())}</b>", ParagraphStyle("BoxHead", fontName="ErnosBold", fontSize=8, leading=10, textColor=colors.white, alignment=TA_CENTER))],
        [Paragraph(inline_markup(args.result), ParagraphStyle("BoxResult", fontName="Ernos", fontSize=11, leading=15, textColor=NAVY, alignment=TA_CENTER))],
    ]
    box = Table(box_data, colWidths=[164 * mm], rowHeights=[9 * mm, 24 * mm])
    box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), TEAL),
        ("BACKGROUND", (0, 1), (-1, -1), CYAN),
        ("BOX", (0, 0), (-1, -1), 0.8, TEAL),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.extend([box, Spacer(1, 12 * mm)])
    story.append(
        Paragraph(
            inline_markup(args.cover_claim),
            ParagraphStyle("CoverClaim", fontName="Ernos", fontSize=10.2, leading=15, textColor=TEXT, alignment=TA_CENTER, leftIndent=13 * mm, rightIndent=13 * mm, spaceAfter=12),
        )
    )
    story.append(Paragraph("OPEN PAPER · OPEN SOURCE · MACHINE-CHECKED EVIDENCE", ParagraphStyle("Open", fontName="ErnosBold", fontSize=8.5, leading=11, textColor=TEAL, alignment=TA_CENTER)))
    story.append(PageBreak())
    return story


def contents(headings: list[tuple[int, str]], styles: dict[str, ParagraphStyle]) -> list:
    flow = [Paragraph("Contents", styles["h1"]), Spacer(1, 2 * mm)]
    for level, title in headings:
        if title in {"Abstract", "The achieved foundation"}:
            continue
        prefix = "&nbsp;&nbsp;&nbsp;" if level >= 3 else ""
        flow.append(Paragraph(prefix + inline_markup(title), styles["toc"]))
    flow.append(PageBreak())
    return flow


def parse_table(lines: list[str], styles: dict[str, ParagraphStyle], width: float) -> list:
    raw = [[cell.strip() for cell in line.strip().strip("|").split("|")] for line in lines]
    raw = [row for row in raw if not all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in row)]
    cols = max(len(row) for row in raw)
    for row in raw:
        row.extend([""] * (cols - len(row)))
    fractions = {
        2: [0.32, 0.68],
        3: [0.20, 0.35, 0.45],
        4: [0.18, 0.25, 0.27, 0.30],
        5: [0.13, 0.21, 0.20, 0.23, 0.23],
    }.get(cols, [1 / cols] * cols)
    cell_style = ParagraphStyle("TableCell", parent=styles["body"], fontSize=7.1, leading=9, spaceAfter=0)
    head_style = ParagraphStyle("TableHead", parent=cell_style, fontName="ErnosBold", textColor=colors.white)
    data = [[Paragraph(inline_markup(cell), head_style if ridx == 0 else cell_style) for cell in row] for ridx, row in enumerate(raw)]
    table = LongTable(data, colWidths=[width * f for f in fractions], repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]),
        ("GRID", (0, 0), (-1, -1), 0.35, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return [table, Spacer(1, 7)]


def markdown_story(text: str, styles: dict[str, ParagraphStyle], doc_width: float) -> list:
    lines = text.splitlines()
    start = next((i for i, line in enumerate(lines) if line.strip() == "## Abstract"), 0)
    lines = lines[start:]
    flow: list = []
    i = 0
    abstract_mode = False
    while i < len(lines):
        stripped = lines[i].strip()
        if not stripped or stripped == "---":
            i += 1
            continue
        if stripped.startswith("```"):
            code = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i].rstrip())
                i += 1
            i += 1
            flow.append(Preformatted("\n".join(code), styles["code"], maxLineLength=115))
            continue
        if stripped in {"\\[", "$$"}:
            closer = "\\]" if stripped == "\\[" else "$$"
            formula = []
            i += 1
            while i < len(lines) and lines[i].strip() != closer:
                formula.append(lines[i].strip())
                i += 1
            i += 1
            flow.append(Paragraph(html.escape(formula_text(" ".join(formula))), styles["formula"]))
            continue
        if stripped.startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            flow.extend(parse_table(table_lines, styles, doc_width))
            continue
        heading = re.match(r"^(#{1,4})\s+(.*)$", stripped)
        if heading:
            level = len(heading.group(1))
            title = heading.group(2)
            abstract_mode = title == "Abstract"
            style = styles["h1"] if level == 1 else styles["h2"] if level == 2 else styles["h3"]
            flow.append(Paragraph(inline_markup(title), style))
            i += 1
            continue
        bullet = re.match(r"^(-|\d+\.)\s+(.*)$", stripped)
        if bullet:
            marker, body = bullet.groups()
            i += 1
            continuation = []
            while i < len(lines):
                candidate = lines[i].strip()
                if not candidate or candidate.startswith(("#", "|", "```", "\\[", "$$")) or re.match(r"^(-|\d+\.)\s+", candidate):
                    break
                continuation.append(candidate)
                i += 1
            body = " ".join([body] + continuation)
            symbol = "•" if marker == "-" else marker
            flow.append(Paragraph(inline_markup(body), styles["bullet"], bulletText=symbol))
            continue
        if stripped.startswith(">"):
            quote = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip().lstrip("> "))
                i += 1
            flow.append(Paragraph(inline_markup(" ".join(quote)), styles["quote"]))
            continue
        paragraph = [stripped]
        i += 1
        while i < len(lines):
            candidate = lines[i].strip()
            if not candidate or candidate.startswith(("#", "|", "```", "\\[", "$$", ">")) or re.match(r"^(-|\d+\.)\s+", candidate):
                break
            paragraph.append(candidate)
            i += 1
        style = styles["abstract"] if abstract_mode else styles["body"]
        flow.append(Paragraph(inline_markup(" ".join(paragraph)), style))
    return flow


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--short-title", required=True)
    parser.add_argument("--subtitle", required=True)
    parser.add_argument("--doi", required=True)
    parser.add_argument("--date", default="22 July 2026")
    parser.add_argument("--edition", required=True)
    parser.add_argument("--result-label", required=True)
    parser.add_argument("--result", required=True)
    parser.add_argument("--cover-claim", required=True)
    parser.add_argument("--keywords", default="Smithian Fold Theory, machine-checked derivation, zero axioms, zero parameters")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    register_fonts()
    source = Path(args.source)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    text = source.read_text(encoding="utf-8")
    headings = []
    for line in text.splitlines():
        match = re.match(r"^(#{1,4})\s+(.*)$", line)
        if match and len(match.group(1)) >= 2:
            headings.append((len(match.group(1)), match.group(2)))
    styles = make_styles()
    doc = PublicationDoc(str(output), args)
    story = cover(args)
    story.extend(contents(headings, styles))
    story.extend(markdown_story(text, styles, doc.width))
    doc.build(story)
    print(output)


if __name__ == "__main__":
    main()
