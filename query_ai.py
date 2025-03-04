import google.generativeai as genai
import logging
from content import get_response_format
from prompts import get_prompt

# Configure logging
logging.basicConfig(level=logging.INFO)

# Set up Gemini API Key (Replace with your API Key)
GEMINI_API_KEY = "AIzaSyDamAcIzDCzgmr7A7T0Mj3xmi4qTiu7BcU"
genai.configure(api_key=GEMINI_API_KEY)

def query_gemini(prompt, query_type="default"):
    """
    Queries Gemini AI and returns a formatted response.
    """
    try:
        model = genai.GenerativeModel(model_name="gemini-2.0-flash-lite")

        # Add structured prompt formatting
        structured_prompt = get_prompt(prompt.lower())
        full_prompt = f"{structured_prompt}\n\nFormat your response clearly.\n\nUser Query: {prompt}"

        # Generate response
        response = model.generate_content(full_prompt)
        response_text = response.text.strip() if response.text else "I couldn't generate a response."

        return format_response(response_text, query_type)

    except Exception as e:
        logging.error(f"Gemini API error: {e}")
        return "Sorry, an error occurred while generating a response."

def format_response(response_text, query_type="default"):
    """
    Formats AI responses based on the query type using content.py rules.
    """
    response_template = get_response_format(query_type)

    if not isinstance(response_template, str):
        logging.error("Invalid response format: response_templates should be a dictionary string.")
        return response_text  # Return unformatted response as fallback

    formatted_response = response_template.replace("{response}", response_text)

    # Preserve new lines for bullet points
    if query_type in ["bullet_points", "points_with_paragraph"]:
        formatted_response = formatted_response.replace("\\n", "\n")

    return formatted_response
