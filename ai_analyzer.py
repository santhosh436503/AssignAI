
import os
import logging

import streamlit as st
from dotenv import load_dotenv
from google import genai

# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

# Read Streamlit Cloud Secrets if .env key is unavailable
if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        api_key = None

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is missing. "
        "Configure it in .env or Streamlit Cloud Secrets."
    )

# =========================================================
# GEMINI CLIENT
# =========================================================

client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-3.8-flash"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =========================================================
# COMMON GEMINI RESPONSE FUNCTION
# =========================================================

def get_gemini_response(prompt):

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        if not response.text:
            return "The AI returned an empty response. Please try again."

        return response.text

    except Exception as e:

        error_message = str(e)
        logger.exception("Gemini API request failed")

        if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
            return (
                "⚠️ Gemini API quota or rate limit reached.\n\n"
                "Please check your Google AI Studio usage and try again "
                "when your quota becomes available."
            )

        if "503" in error_message or "UNAVAILABLE" in error_message:
            return (
                "⚠️ Gemini AI is temporarily unavailable or experiencing "
                "high demand.\n\nPlease try again later."
            )

        if "404" in error_message or "NOT_FOUND" in error_message:
            return (
                f"❌ Gemini model '{MODEL_NAME}' was not found or is "
                "unavailable for this API key. Check the model name."
            )

        if "403" in error_message or "PERMISSION_DENIED" in error_message:
            return (
                "❌ Gemini API access denied. Check your API key, "
                "project permissions and API configuration."
            )

        return (
            "❌ Gemini request failed.\n\n"
            f"Error details: {error_message}"
        )


# =========================================================
# ANALYZE ASSIGNMENT
# =========================================================

def analyze_assignment(text):

    prompt = f"""
You are an academic assignment analyzer.

Analyze the following assignment questions.

Provide:

1. Subject
2. Main topic
3. Question types
4. Difficulty level
5. Important concepts
6. Suggested answer structure

Keep the analysis clear and simple.

Assignment questions:

{text}
"""

    return get_gemini_response(prompt)


# =========================================================
# GENERATE ASSIGNMENT
# =========================================================

def generate_assignment(text, answer_length):

    prompt = f"""
You are an academic assignment assistant.

Create a well-structured educational assignment based on
the questions provided below.

Answer length: {answer_length}

Requirements:

- Answer every question.
- Use clear headings.
- Use simple academic language.
- Explain concepts clearly.
- Include examples where useful.
- Number the questions.
- Include an introduction.
- Include a conclusion.
- Make the content suitable for a college student.
- Do not mention that AI generated the assignment.

Assignment questions:

{text}
"""

    return get_gemini_response(prompt)
