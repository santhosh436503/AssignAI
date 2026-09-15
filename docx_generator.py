from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH


def create_assignment_docx(
    assignment_text,
    student_name,
    subject,
    college_name,
    assignment_title
):

    file_path = "AssignAI_Assignment.docx"

    document = Document()

    # ==========================================
    # COVER PAGE
    # ==========================================

    title = document.add_paragraph()

    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    run = title.add_run("ASSIGNAI")
    run.bold = True
    run.font.size = Pt(28)

    subtitle = document.add_paragraph()

    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER

    run = subtitle.add_run(
        "AI-Powered Assignment Analyzer & Generator"
    )
    run.font.size = Pt(14)

    document.add_paragraph("")

    assignment = document.add_paragraph()

    assignment.alignment = WD_ALIGN_PARAGRAPH.CENTER

    run = assignment.add_run(assignment_title)
    run.bold = True
    run.font.size = Pt(20)

    document.add_paragraph("")

    # Student details

    details = [
        ("Student Name", student_name),
        ("Subject", subject),
        ("College", college_name)
    ]

    for label, value in details:

        paragraph = document.add_paragraph()

        run = paragraph.add_run(
            f"{label}: "
        )
        run.bold = True

        paragraph.add_run(value)

    document.add_page_break()

    # ==========================================
    # ASSIGNMENT CONTENT
    # ==========================================

    heading = document.add_paragraph()

    heading.alignment = WD_ALIGN_PARAGRAPH.CENTER

    run = heading.add_run(assignment_title)
    run.bold = True
    run.font.size = Pt(18)

    document.add_paragraph("")

    # Add assignment text

    for line in assignment_text.split("\n"):

        line = line.strip()

        if not line:
            continue

        # Remove Markdown symbols

        line = line.replace("**", "")
        line = line.replace("*", "")

        # Question headings

        if line.lower().startswith("question"):

            paragraph = document.add_paragraph()

            run = paragraph.add_run(line)
            run.bold = True
            run.font.size = Pt(14)

        elif line.lower() in [
            "introduction",
            "conclusion",
            "references",
            "advantages",
            "disadvantages"
        ]:

            paragraph = document.add_paragraph()

            run = paragraph.add_run(line)
            run.bold = True
            run.font.size = Pt(14)

        else:

            paragraph = document.add_paragraph(line)

            for run in paragraph.runs:
                run.font.size = Pt(11)

    # ==========================================
    # SAVE
    # ==========================================

    document.save(file_path)

    return file_path