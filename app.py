import os
import json
import zipfile

import streamlit as st
from PIL import Image

from pdf_processor import extract_text_from_pdf
from ai_analyzer import analyze_assignment, generate_assignment
from pdf_generator import create_assignment_pdf
from docx_generator import create_assignment_docx
from ocr_processor import extract_text_from_image


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AssignAI",
    page_icon="📚",
    layout="wide"
)


# =========================================================
# HISTORY FILE
# =========================================================

HISTORY_FILE = "assignment_history.json"


def load_history():
    """Load assignment history from JSON."""

    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if isinstance(data, list):
            return data

        return []

    except Exception:
        return []


def save_history(history):
    """Save assignment history to JSON."""

    try:
        with open(
            HISTORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                history,
                file,
                indent=4,
                ensure_ascii=False
            )

    except Exception as e:

        st.error(
            f"❌ Could not save history: {e}"
        )


# =========================================================
# CREATE ZIP FILE
# =========================================================

def create_download_zip(pdf_file, docx_file):
    """Create ZIP containing PDF and DOCX."""

    zip_file = "AssignAI_Assignment_Package.zip"

    with zipfile.ZipFile(
        zip_file,
        "w",
        zipfile.ZIP_DEFLATED
    ) as zipf:

        zipf.write(
            pdf_file,
            "AssignAI_Assignment.pdf"
        )

        zipf.write(
            docx_file,
            "AssignAI_Assignment.docx"
        )

    return zip_file


# =========================================================
# SESSION STATE
# =========================================================

if "extracted_text" not in st.session_state:
    st.session_state["extracted_text"] = ""

if "analysis" not in st.session_state:
    st.session_state["analysis"] = ""

if "assignment" not in st.session_state:
    st.session_state["assignment"] = ""

if "student_name" not in st.session_state:
    st.session_state["student_name"] = ""

if "subject" not in st.session_state:
    st.session_state["subject"] = ""

if "college_name" not in st.session_state:
    st.session_state["college_name"] = ""

if "assignment_title" not in st.session_state:
    st.session_state["assignment_title"] = ""

if "history" not in st.session_state:
    st.session_state["history"] = load_history()


# =========================================================
# DASHBOARD VALUES
# =========================================================

total_assignments = len(
    st.session_state.get(
        "history",
        []
    )
)

has_analysis = bool(
    st.session_state.get(
        "analysis",
        ""
    )
)

has_assignment = bool(
    st.session_state.get(
        "assignment",
        ""
    )
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 44px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 25px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("📚 AssignAI")

    st.write(
        "AI-Powered Assignment Analyzer & Generator"
    )

    st.divider()

    st.subheader("🚀 Workflow")

    st.write("1️⃣ Upload / Enter Questions")
    st.write("2️⃣ Extract Text")
    st.write("3️⃣ AI Analysis")
    st.write("4️⃣ Generate Assignment")
    st.write("5️⃣ Edit Assignment")
    st.write("6️⃣ Download PDF / DOCX")
    st.write("7️⃣ Download Complete ZIP")
    st.write("8️⃣ View History")

    st.divider()

    st.subheader("✨ Features")

    st.write("📄 PDF Support")
    st.write("📝 TXT Support")
    st.write("📸 Image OCR")
    st.write("🤖 AI Analysis")
    st.write("✍️ Assignment Generation")
    st.write("✏️ Assignment Editing")
    st.write("🔄 Regeneration")
    st.write("📄 PDF Export")
    st.write("📝 DOCX Export")
    st.write("📦 ZIP Download")
    st.write("🕘 Persistent History")


# =========================================================
# DASHBOARD
# =========================================================

st.subheader("📊 AssignAI Dashboard")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "📚 Assignments",
        total_assignments
    )

with col2:

    st.metric(
        "🧠 AI Analysis",
        "Ready" if has_analysis else "Pending"
    )

with col3:

    st.metric(
        "✍️ Assignment",
        "Ready" if has_assignment else "Pending"
    )

with col4:

    st.metric(
        "📥 Downloads",
        "PDF + DOCX"
    )


st.divider()


# =========================================================
# MAIN HEADER
# =========================================================

st.markdown(
    '<div class="main-title">📚 AssignAI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    "AI-Powered Assignment Analyzer & Generator"
    "</div>",
    unsafe_allow_html=True
)

st.write(
    "Upload your assignment questions or enter them manually. "
    "AssignAI will analyze the questions and generate "
    "a structured college assignment."
)

st.divider()


# =========================================================
# TABS
# =========================================================

tab_input, tab_analysis, tab_assignment, tab_download, tab_history = st.tabs(
    [
        "📤 Input",
        "🧠 Analysis",
        "📚 Assignment",
        "📥 Download",
        "🕘 History"
    ]
)


# =========================================================
# TAB 1 — INPUT
# =========================================================

with tab_input:

    st.header("📤 Assignment Input")

    st.write(
        "Upload a PDF, text file, image, or enter questions manually."
    )

    # -----------------------------------------------------
    # FILE UPLOAD
    # -----------------------------------------------------

    st.subheader("📁 Upload Assignment")

    uploaded_file = st.file_uploader(
        "Upload PDF, TXT or Image",
        type=[
            "pdf",
            "txt",
            "png",
            "jpg",
            "jpeg"
        ]
    )

    if uploaded_file is not None:

        st.success(
            f"✅ Uploaded: {uploaded_file.name}"
        )

        # =================================================
        # PDF
        # =================================================

        if uploaded_file.type == "application/pdf":

            try:

                uploaded_file.seek(0)

                extracted_text = extract_text_from_pdf(
                    uploaded_file
                )

                st.session_state[
                    "extracted_text"
                ] = extracted_text

                st.subheader(
                    "📄 Extracted Questions"
                )

                if extracted_text.strip():

                    st.text_area(
                        "Text extracted from PDF:",
                        extracted_text,
                        height=300,
                        key="pdf_text_preview"
                    )

                else:

                    st.warning(
                        "⚠️ No readable text was found in this PDF."
                    )

            except Exception as e:

                st.error(
                    f"❌ PDF processing failed: {e}"
                )

        # =================================================
        # TXT
        # =================================================

        elif uploaded_file.type == "text/plain":

            try:

                extracted_text = uploaded_file.read().decode(
                    "utf-8"
                )

                st.session_state[
                    "extracted_text"
                ] = extracted_text

                st.subheader(
                    "📄 Text File Content"
                )

                st.text_area(
                    "Questions from text file:",
                    extracted_text,
                    height=300,
                    key="txt_text_preview"
                )

            except Exception as e:

                st.error(
                    f"❌ TXT processing failed: {e}"
                )

        # =================================================
        # IMAGE OCR
        # =================================================

        elif uploaded_file.type in [
            "image/png",
            "image/jpeg"
        ]:

            try:

                image = Image.open(
                    uploaded_file
                )

                st.subheader(
                    "🖼️ Uploaded Assignment Image"
                )

                st.image(
                    image,
                    caption="Uploaded Assignment",
                    use_container_width=True
                )

                with st.spinner(
                    "🔍 Extracting text from image..."
                ):

                    extracted_text = extract_text_from_image(
                        image
                    )

                st.session_state[
                    "extracted_text"
                ] = extracted_text

                st.subheader(
                    "🔍 OCR Extracted Text"
                )

                if extracted_text.strip():

                    st.text_area(
                        "Text extracted from image:",
                        extracted_text,
                        height=300,
                        key="ocr_text_preview"
                    )

                    st.success(
                        "✅ OCR completed successfully!"
                    )

                else:

                    st.warning(
                        "⚠️ No readable text was found in this image."
                    )

            except Exception as e:

                st.error(
                    f"❌ OCR failed: {e}"
                )

    # =====================================================
    # MANUAL INPUT
    # =====================================================

    st.divider()

    st.subheader(
        "📝 Or Enter Questions Manually"
    )

    questions = st.text_area(
        "Paste your assignment questions here:",
        height=200,
        placeholder=(
            "Example:\n"
            "1. Explain Artificial Intelligence.\n"
            "2. Explain applications of AI in healthcare.\n"
            "3. Explain advantages and disadvantages of AI."
        ),
        key="manual_questions"
    )

    if questions.strip():

        st.session_state[
            "extracted_text"
        ] = questions

    # =====================================================
    # ANALYZE
    # =====================================================

    st.divider()

    if st.button(
        "🔍 Analyze Assignment",
        type="primary",
        use_container_width=True
    ):

        assignment_text = st.session_state[
            "extracted_text"
        ]

        if not assignment_text.strip():

            st.warning(
                "⚠️ Please upload a file or enter questions first."
            )

        else:

            with st.spinner(
                "🤖 AI is analyzing your assignment..."
            ):

                try:

                    analysis = analyze_assignment(
                        assignment_text
                    )

                    st.session_state[
                        "analysis"
                    ] = analysis

                    if (
                        analysis.startswith("❌")
                        or analysis.startswith("⚠️")
                    ):

                        st.warning(
                            analysis
                        )

                    else:

                        st.success(
                            "✅ Assignment analyzed successfully!"
                        )

                        st.info(
                            "👉 Open the 🧠 Analysis tab."
                        )

                except Exception as e:

                    st.error(
                        f"❌ AI analysis failed: {e}"
                    )


# =========================================================
# TAB 2 — ANALYSIS
# =========================================================

with tab_analysis:

    st.header("🧠 AI Analysis")

    if st.session_state["analysis"]:

        st.write(
            st.session_state["analysis"]
        )

    else:

        st.info(
            "📌 No analysis available yet."
        )

        st.write(
            "Go to the 📤 Input tab and analyze your questions."
        )


# =========================================================
# TAB 3 — ASSIGNMENT
# =========================================================

with tab_assignment:

    st.header("📚 Generate Assignment")

    if not st.session_state[
        "extracted_text"
    ].strip():

        st.info(
            "📌 First enter or upload your assignment questions."
        )

    else:

        st.subheader(
            "👤 Assignment Details"
        )

        student_name = st.text_input(
            "Student Name",
            value=st.session_state[
                "student_name"
            ]
        )

        subject = st.text_input(
            "Subject",
            value=st.session_state[
                "subject"
            ]
        )

        college_name = st.text_input(
            "College Name",
            value=st.session_state[
                "college_name"
            ]
        )

        assignment_title = st.text_input(
            "Assignment Title",
            value=(
                st.session_state[
                    "assignment_title"
                ]
                or "AI Generated Assignment"
            )
        )

        st.subheader(
            "📏 Answer Length"
        )

        answer_length = st.selectbox(
            "Choose answer length:",
            [
                "Short",
                "Medium",
                "Detailed"
            ]
        )

        st.divider()

        # =================================================
        # GENERATE
        # =================================================

        if st.button(
            "✍️ Generate Assignment",
            type="primary",
            use_container_width=True
        ):

            assignment_text = st.session_state[
                "extracted_text"
            ]

            with st.spinner(
                "🤖 Generating your assignment..."
            ):

                try:

                    assignment = generate_assignment(
                        assignment_text,
                        answer_length
                    )

                    if (
                        assignment.startswith("❌")
                        or assignment.startswith("⚠️")
                    ):

                        st.warning(
                            assignment
                        )

                    else:

                        st.session_state[
                            "assignment"
                        ] = assignment

                        st.session_state[
                            "student_name"
                        ] = student_name

                        st.session_state[
                            "subject"
                        ] = subject

                        st.session_state[
                            "college_name"
                        ] = college_name

                        st.session_state[
                            "assignment_title"
                        ] = assignment_title

                        history_item = {
                            "title": assignment_title,
                            "student": student_name,
                            "subject": subject,
                            "college": college_name,
                            "content": assignment
                        }

                        st.session_state[
                            "history"
                        ].append(
                            history_item
                        )

                        save_history(
                            st.session_state[
                                "history"
                            ]
                        )

                        st.success(
                            "✅ Assignment generated successfully!"
                        )

                except Exception as e:

                    st.error(
                        f"❌ Assignment generation failed: {e}"
                    )

        # =================================================
        # DISPLAY ASSIGNMENT
        # =================================================

        if st.session_state[
            "assignment"
        ]:

            st.divider()

            st.subheader(
                "📖 Generated Assignment"
            )

            edited_assignment = st.text_area(
                "✏️ Edit your assignment:",
                value=st.session_state[
                    "assignment"
                ],
                height=500,
                key="assignment_editor"
            )

            if st.button(
                "💾 Save Changes",
                use_container_width=True
            ):

                st.session_state[
                    "assignment"
                ] = edited_assignment

                if st.session_state[
                    "history"
                ]:

                    st.session_state[
                        "history"
                    ][-1]["content"] = edited_assignment

                    save_history(
                        st.session_state[
                            "history"
                        ]
                    )

                st.success(
                    "✅ Assignment changes saved!"
                )

            st.divider()

            col1, col2 = st.columns(2)

            # =================================================
            # REGENERATE
            # =================================================

            with col1:

                if st.button(
                    "🔄 Regenerate Assignment",
                    use_container_width=True
                ):

                    assignment_text = st.session_state[
                        "extracted_text"
                    ]

                    with st.spinner(
                        "🤖 Generating a new version..."
                    ):

                        try:

                            new_assignment = generate_assignment(
                                assignment_text,
                                answer_length
                            )

                            if (
                                new_assignment.startswith("❌")
                                or new_assignment.startswith("⚠️")
                            ):

                                st.warning(
                                    new_assignment
                                )

                            else:

                                st.session_state[
                                    "assignment"
                                ] = new_assignment

                                st.session_state[
                                    "history"
                                ].append(
                                    {
                                        "title": assignment_title,
                                        "student": student_name,
                                        "subject": subject,
                                        "college": college_name,
                                        "content": new_assignment
                                    }
                                )

                                save_history(
                                    st.session_state[
                                        "history"
                                    ]
                                )

                                st.success(
                                    "✅ New assignment generated!"
                                )

                                st.rerun()

                        except Exception as e:

                            st.error(
                                f"❌ Regeneration failed: {e}"
                            )

            # =================================================
            # NEW ASSIGNMENT
            # =================================================

            with col2:

                if st.button(
                    "🆕 Start New Assignment",
                    use_container_width=True
                ):

                    st.session_state[
                        "extracted_text"
                    ] = ""

                    st.session_state[
                        "analysis"
                    ] = ""

                    st.session_state[
                        "assignment"
                    ] = ""

                    st.session_state[
                        "student_name"
                    ] = ""

                    st.session_state[
                        "subject"
                    ] = ""

                    st.session_state[
                        "college_name"
                    ] = ""

                    st.session_state[
                        "assignment_title"
                    ] = ""

                    st.success(
                        "✅ Ready for a new assignment!"
                    )

                    st.rerun()


# =========================================================
# TAB 4 — DOWNLOAD
# =========================================================

with tab_download:

    st.header(
        "📥 Download Assignment"
    )

    if not st.session_state[
        "assignment"
    ]:

        st.info(
            "📌 Generate an assignment first."
        )

    else:

        student_name = st.session_state.get(
            "student_name",
            "Student"
        )

        subject = st.session_state.get(
            "subject",
            "Subject"
        )

        college_name = st.session_state.get(
            "college_name",
            "College"
        )

        assignment_title = st.session_state.get(
            "assignment_title",
            "AI Generated Assignment"
        )

        assignment_text = st.session_state[
            "assignment"
        ]

        # =================================================
        # PDF
        # =================================================

        st.subheader(
            "📄 PDF Assignment"
        )

        if st.button(
            "📄 Generate PDF",
            type="primary",
            use_container_width=True
        ):

            with st.spinner(
                "📄 Creating PDF..."
            ):

                try:

                    pdf_file = create_assignment_pdf(
                        assignment_text,
                        student_name,
                        subject,
                        college_name,
                        assignment_title
                    )

                    st.success(
                        "✅ PDF created successfully!"
                    )

                    with open(
                        pdf_file,
                        "rb"
                    ) as file:

                        pdf_data = file.read()

                    st.download_button(
                        label="⬇️ Download PDF",
                        data=pdf_data,
                        file_name="AssignAI_Assignment.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

                except Exception as e:

                    st.error(
                        f"❌ PDF generation failed: {e}"
                    )

        st.divider()

        # =================================================
        # DOCX
        # =================================================

        st.subheader(
            "📝 Word Document"
        )

        if st.button(
            "📝 Generate DOCX",
            use_container_width=True
        ):

            with st.spinner(
                "📝 Creating Word document..."
            ):

                try:

                    docx_file = create_assignment_docx(
                        assignment_text,
                        student_name,
                        subject,
                        college_name,
                        assignment_title
                    )

                    st.success(
                        "✅ Word document created successfully!"
                    )

                    with open(
                        docx_file,
                        "rb"
                    ) as file:

                        docx_data = file.read()

                    st.download_button(
                        label="⬇️ Download DOCX",
                        data=docx_data,
                        file_name="AssignAI_Assignment.docx",
                        mime=(
                            "application/vnd.openxmlformats-"
                            "officedocument.wordprocessingml.document"
                        ),
                        use_container_width=True
                    )

                except Exception as e:

                    st.error(
                        f"❌ DOCX generation failed: {e}"
                    )

        # =================================================
        # DOWNLOAD ALL
        # =================================================

        st.divider()

        st.subheader(
            "📦 Complete Assignment Package"
        )

        if st.button(
            "📦 Create ZIP — PDF + DOCX",
            use_container_width=True
        ):

            with st.spinner(
                "📦 Creating complete package..."
            ):

                try:

                    pdf_file = create_assignment_pdf(
                        assignment_text,
                        student_name,
                        subject,
                        college_name,
                        assignment_title
                    )

                    docx_file = create_assignment_docx(
                        assignment_text,
                        student_name,
                        subject,
                        college_name,
                        assignment_title
                    )

                    zip_file = create_download_zip(
                        pdf_file,
                        docx_file
                    )

                    with open(
                        zip_file,
                        "rb"
                    ) as file:

                        zip_data = file.read()

                    st.success(
                        "✅ Complete package created!"
                    )

                    st.download_button(
                        label="⬇️ Download PDF + DOCX",
                        data=zip_data,
                        file_name="AssignAI_Assignment_Package.zip",
                        mime="application/zip",
                        use_container_width=True
                    )

                except Exception as e:

                    st.error(
                        f"❌ Package creation failed: {e}"
                    )


# =========================================================
# TAB 5 — HISTORY
# =========================================================

with tab_history:

    st.header(
        "🕘 Assignment History"
    )

    history = st.session_state.get(
        "history",
        []
    )

    if not history:

        st.info(
            "📌 No assignments generated yet."
        )

    else:

        st.success(
            f"📚 Total assignments: {len(history)}"
        )

        if st.button(
            "🗑️ Clear All History",
            use_container_width=True
        ):

            st.session_state[
                "history"
            ] = []

            save_history([])

            st.success(
                "✅ Assignment history cleared!"
            )

            st.rerun()

        st.divider()

        for index, item in enumerate(
            reversed(history),
            start=1
        ):

            title = item.get(
                "title",
                "Untitled Assignment"
            )

            subject_name = item.get(
                "subject",
                "Unknown Subject"
            )

            with st.expander(
                f"📄 {title} — {subject_name}"
            ):

                st.write(
                    f"👤 Student: {item.get('student', '')}"
                )

                st.write(
                    f"📚 Subject: {subject_name}"
                )

                st.write(
                    f"🏫 College: {item.get('college', '')}"
                )

                st.divider()

                st.text_area(
                    "Assignment:",
                    item.get(
                        "content",
                        ""
                    ),
                    height=300,
                    key=f"history_assignment_{index}"
                )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "📚 AssignAI — AI-Powered Assignment Analyzer & Generator"
)

