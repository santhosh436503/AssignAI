import os

from dotenv import load_dotenv
from google import genai


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is not set in the .env file."
    )


# =========================================================
# GEMINI CLIENT
# =========================================================

client = genai.Client(
    api_key=api_key
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

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        error_message = str(e)

        if (
            "429" in error_message
            or "RESOURCE_EXHAUSTED" in error_message
        ):

            return (
                "⚠️ Gemini API quota has been temporarily "
                "exceeded.\n\n"
                "Please wait and try again later."
            )

        if (
            "503" in error_message
            or "UNAVAILABLE" in error_message
        ):

            return (
                "⚠️ Gemini AI is currently experiencing "
                "high demand.\n\n"
                "Please wait a little and try again."
            )

        return (
            "❌ AI analysis failed.\n\n"
            f"Error: {error_message}"
        )


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

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        error_message = str(e)

        if (
            "429" in error_message
            or "RESOURCE_EXHAUSTED" in error_message
        ):

            return (
                "⚠️ Gemini API quota has been temporarily "
                "exceeded.\n\n"
                "Please wait and try again later."
            )

        if (
            "503" in error_message
            or "UNAVAILABLE" in error_message
        ):

            return (
                "⚠️ Gemini AI is currently experiencing "
                "high demand.\n\n"
                "Please wait a little and try again."
            )

        return (
            "❌ Assignment generation failed.\n\n"
            f"Error: {error_message}"
        )

