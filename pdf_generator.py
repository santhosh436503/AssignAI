from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    KeepTogether
)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.colors import HexColor
import os
import re


# =========================================================
# PDF OUTPUT LOCATION
# =========================================================

OUTPUT_FILE = "AssignAI_Assignment.pdf"


# =========================================================
# PAGE NUMBER
# =========================================================

def add_page_number(canvas, document):

    canvas.saveState()

    canvas.setFont("Helvetica", 9)

    canvas.drawCentredString(
        A4[0] / 2,
        12 * mm,
        f"Page {document.page}"
    )

    canvas.restoreState()


# =========================================================
# CLEAN TEXT
# =========================================================

def clean_text(text):

    if not text:
        return ""

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    return text.strip()


# =========================================================
# CONVERT MARKDOWN-LIKE TEXT
# =========================================================

def format_inline_text(text):

    text = text.replace(
        "**",
        ""
    )

    text = text.replace(
        "__",
        ""
    )

    return text.strip()


# =========================================================
# CREATE ASSIGNMENT PDF
# =========================================================

def create_assignment_pdf(
    assignment_text,
    student_name,
    subject,
    college_name,
    assignment_title
):

    assignment_text = clean_text(
        assignment_text
    )

    # -----------------------------------------------------
    # Create PDF document
    # -----------------------------------------------------

    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm
    )

    # -----------------------------------------------------
    # Styles
    # -----------------------------------------------------

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=30,
        alignment=TA_CENTER,
        spaceAfter=10
    )

    subtitle_style = ParagraphStyle(
        "SubtitleStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=13,
        leading=18,
        alignment=TA_CENTER,
        spaceAfter=20
    )

    info_style = ParagraphStyle(
        "InfoStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=18,
        alignment=TA_LEFT,
        spaceAfter=4
    )

    heading_style = ParagraphStyle(
        "HeadingStyle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=22,
        spaceBefore=14,
        spaceAfter=8
    )

    question_style = ParagraphStyle(
        "QuestionStyle",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=19,
        spaceBefore=12,
        spaceAfter=6
    )

    answer_style = ParagraphStyle(
        "AnswerStyle",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=11,
        leading=17,
        alignment=TA_LEFT,
        spaceAfter=8
    )

    normal_style = ParagraphStyle(
        "NormalStyle",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=11,
        leading=17,
        alignment=TA_LEFT,
        spaceAfter=8
    )

    # -----------------------------------------------------
    # Story
    # -----------------------------------------------------

    story = []

    # =====================================================
    # COVER PAGE
    # =====================================================

    story.append(
        Spacer(
            1,
            35 * mm
        )
    )

    story.append(
        Paragraph(
            "📚 AssignAI",
            title_style
        )
    )

    story.append(
        Paragraph(
            "AI-Powered Assignment",
            subtitle_style
        )
    )

    story.append(
        Spacer(
            1,
            15 * mm
        )
    )

    story.append(
        Paragraph(
            f"<b>{format_inline_text(assignment_title)}</b>",
            heading_style
        )
    )

    story.append(
        Spacer(
            1,
            10 * mm
        )
    )

    # -----------------------------------------------------
    # Student information
    # -----------------------------------------------------

    if student_name:

        story.append(
            Paragraph(
                f"<b>Student Name:</b> "
                f"{format_inline_text(student_name)}",
                info_style
            )
        )

    if subject:

        story.append(
            Paragraph(
                f"<b>Subject:</b> "
                f"{format_inline_text(subject)}",
                info_style
            )
        )

    if college_name:

        story.append(
            Paragraph(
                f"<b>College:</b> "
                f"{format_inline_text(college_name)}",
                info_style
            )
        )

    story.append(
        Spacer(
            1,
            25 * mm
        )
    )

    story.append(
        Paragraph(
            "Generated using AssignAI",
            subtitle_style
        )
    )

    story.append(
        PageBreak()
    )

    # =====================================================
    # ASSIGNMENT CONTENT
    # =====================================================

    lines = assignment_text.split("\n")

    for line in lines:

        line = line.strip()

        if not line:
            story.append(
                Spacer(1, 4)
            )
            continue

        clean_line = format_inline_text(
            line
        )

        # -------------------------------------------------
        # Main headings
        # -------------------------------------------------

        if re.match(
            r"^(Introduction|Conclusion|References|"
            r"Abstract|Summary)$",
            clean_line,
            re.IGNORECASE
        ):

            story.append(
                Paragraph(
                    clean_line,
                    heading_style
                )
            )

        # -------------------------------------------------
        # Question headings
        # -------------------------------------------------

        elif re.match(
            r"^(Question\s*\d+|Q\.?\s*\d+|\d+\.)",
            clean_line,
            re.IGNORECASE
        ):

            story.append(
                Paragraph(
                    clean_line,
                    question_style
                )
            )

        # -------------------------------------------------
        # Bullet points
        # -------------------------------------------------

        elif clean_line.startswith(
            ("-", "•", "*")
        ):

            bullet_text = clean_line[1:].strip()

            story.append(
                Paragraph(
                    f"• {bullet_text}",
                    answer_style
                )
            )

        # -------------------------------------------------
        # Numbered sub-points
        # -------------------------------------------------

        elif re.match(
            r"^\d+\)",
            clean_line
        ):

            story.append(
                Paragraph(
                    clean_line,
                    answer_style
                )
            )

        # -------------------------------------------------
        # Normal paragraph
        # -------------------------------------------------

        else:

            story.append(
                Paragraph(
                    clean_line,
                    normal_style
                )
            )

    # =====================================================
    # BUILD PDF
    # =====================================================

    doc.build(
        story,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number
    )

    return OUTPUT_FILE

