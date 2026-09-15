import fitz


def extract_text_from_pdf(uploaded_file):
    pdf_bytes = uploaded_file.read()

    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")

    extracted_text = ""

    for page in pdf_document:
        extracted_text += page.get_text()

    pdf_document.close()

    return extracted_text