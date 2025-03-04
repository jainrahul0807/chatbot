from flask import Flask, request, jsonify, render_template,send_from_directory
from flask_cors import CORS
import logging
from query_ai import query_gemini
from knowledge_base import search_knowledge_base, save_to_knowledge_base
from prompts import get_prompt

# Initialize Flask app
app = Flask(__name__, static_folder="static")
CORS(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route("/")
def home():
    # return "Chatbot is running"
    return render_template("index.html")

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_input = data.get("message", "").strip()
        query_type = data.get("format", "default")

        if not user_input:
            return jsonify({"response": "Please provide a valid message."})

        # 🔹 Step 1: Check predefined prompts
        prompt_response = get_prompt(user_input.lower()) or "Let me find an answer for you."

        # 🔹 Step 2: Search the knowledge base
        kb_response = search_knowledge_base(user_input)

        # 🔹 Step 3: Construct final prompt
        final_prompt = f"{prompt_response}\n\nUser Query: {user_input}"
        if kb_response:
            final_prompt = f"{prompt_response}\n\nBased on the knowledge base: {kb_response}\n\nUser Query: {user_input}"

        # 🔹 Step 4: Generate AI response
        response = query_gemini(final_prompt, query_type=query_type)

        # 🔹 Step 5: Save response if it's new
        if not kb_response:
            save_to_knowledge_base(user_input, response)

        return jsonify({"response": response})

    except Exception as e:
        logging.error(f"Error in /chat endpoint: {e}")
        return jsonify({"response": "An error occurred while processing your request."})

@app.route("/script")
def chatbot_script():
    return send_from_directory("static", "index.html")

if __name__ == '__main__':
    from waitress import serve
    # app.run(debug=True)
    serve( app , host="0.0.0.0",port=8000)

# from flask import Flask, request, jsonify, render_template
# import google.generativeai as genai
# import json
# import logging
# from flask_cors import CORS
# from flask import send_from_directory
# from prompts import get_prompt
# from content import get_response_format
#
# # Initialize Flask app
# app = Flask(__name__, static_folder="static")
# CORS(app)
#
# # Configure logging
# logging.basicConfig(level=logging.DEBUG)
#
# # Set up Gemini API Key
# GEMINI_API_KEY = "AIzaSyDamAcIzDCzgmr7A7T0Mj3xmi4qTiu7BcU"
# genai.configure(api_key=GEMINI_API_KEY)
#
# # Load the knowledge base (data.json)
# def load_knowledge_base():
#     """Loads knowledge base from data.json file."""
#     try:
#         with open("data.json", "r", encoding="utf-8") as file:
#             data = json.load(file)
#             logging.info("Knowledge base loaded successfully.")
#             return data
#     except Exception as e:
#         logging.error(f"Failed to load knowledge base: {e}")
#         return {"paragraphs": [], "headings": {}, "links": {}}
#
# knowledge_base = load_knowledge_base()
#
# def query_gemini(prompt, context=None,query_type="default"):
#     """Query the Gemini AI model."""
#     try:
#         model = genai.GenerativeModel(model_name="gemini-2.0-flash-lite")  # Check latest model name
#         structured_prompt=get_prompt(prompt.lower())
#         full_prompt = (
#             f"{structured_prompt}\n\n"
#             f"Format your response with clear sections, bold headings, bullet points, and emojis. "
#             f"Keep it concise and engaging. \n\n"
#             f"Context: {context}\n\nUser Query: {prompt}"
#             if context else f"Format your response in a structured manner using Markdown. \n\nUser Query: {prompt}"
#         )
#         response = model.generate_content(full_prompt)
#         response_text = response.text.strip() if response.text else "I couldn't generate a response."
#         return format_response(response_text, query_type)
#     except Exception as e:
#         logging.error(f"Gemini API error: {e}")
#         return "Sorry, an error occurred while generating a response."
#
#
# def format_response(response_text, query_type="default"):
#     """Formats AI responses based on the query type using content.py rules."""
#     response_template = get_response_format(query_type)
#     if not isinstance(response_template, str):
#         raise TypeError("response_formats should be a dictionary, but found a function or other type.")  # Debugging
#
#     formatted_response = response_template.replace("{response}", response_text)
#
#     # Ensure new lines are preserved correctly for bullet points
#     if query_type in ["bullet_points", "points_with_paragraph"]:
#         formatted_response = formatted_response.replace("\\n", "\n")
#
#     return formatted_response
#
# def search_knowledge_base(query):
#     """Search knowledge base for relevant information."""
#     try:
#         for para in knowledge_base.get("paragraphs", []):
#             if query.lower() in para.lower():
#                 return para
#         for heading_list in knowledge_base.get("headings", {}).values():
#             for heading in heading_list:
#                 if query.lower() in heading.lower():
#                     return heading
#         return None
#     except Exception as e:
#         logging.error(f"Error searching knowledge base: {e}")
#         return None
#
# def save_to_knowledge_base(question, answer):
#     """Save new Gemini AI responses to the knowledge base."""
#     try:
#         knowledge_base["paragraphs"].append(answer)
#         with open("data.json", "w", encoding="utf-8") as file:
#             json.dump(knowledge_base, file, indent=4, ensure_ascii=False)
#         logging.info("New data saved to knowledge base.")
#     except Exception as e:
#         logging.error(f"Failed to save data to knowledge base: {e}")
#
# @app.route("/")
# def home():
#     # return render_template("old.html")
#     return "chatbot is running"
# @app.route('/chat', methods=['POST'])
# def chat():
#     try:
#         data = request.json
#         user_input = data.get("message", "").strip()
#         query_type = data.get("format", "default")
#         if not user_input:
#             return jsonify({"response": "Please provide a valid message."})
#
#         # 🔹 Step 1: Check if the input matches any predefined prompt category
#         prompt_response = get_prompt(user_input.lower()) or "Let me find an answer for you." # Fetch prompt from prompts.py
#         # logging.info(f"Using predefined prompt: {prompt_response}")
#
#         # Step 2: Check knowledge base for relevant data
#         kb_response = search_knowledge_base(user_input)
#
#         # Step 3: If found, enhance it using Gemini AI
#         if kb_response:
#             final_prompt = f"{prompt_response}\n\nBased on the knowledge base: {kb_response}\n\nUser Query: {user_input}"
#         else:
#             final_prompt = f"{prompt_response}\n\nUser Query: {user_input}"
#
#         # 🔹 Step 4: Generate a response from Gemini
#         response = query_gemini(final_prompt,query_type= query_type)
#         # final_response = format_response(response)
#     # 🔹 Step 5: Save the response for future use
#         if not kb_response:
#             save_to_knowledge_base(user_input, response)
#
#         return jsonify({"response": response})
#
#     except Exception as e:
#         logging.error(f"Error in /chat endpoint: {e}")
#         return jsonify({"response": "An error occurred while processing your request."})
#
#     #     if kb_response:
#     #         response = query_gemini(user_input, context=kb_response)
#     #     elif prompt_response:
#     #         response=query_gemini(prompt_response)
#     #     else:
#     #         # Step 4: If not found, get a fresh response from Gemini AI
#     #         response = query_gemini(user_input)
#     #         save_to_knowledge_base(user_input, response)  # Save response for future use
#     #
#     #     return jsonify({"response": response})
#     # except Exception as e:
#     #     logging.error(f"Error in /chat endpoint: {e}")
#     #     return jsonify({"response": "An error occurred while processing your request."})
#
#
# @app.route("/script")
# def chatbot_script():
#     return send_from_directory("static", "chatbot.js")
#
# # Run Flask server
# if __name__ == '__main__':
#     # app.run(host="0.0.0.0", port=5000, debug=True)
#     app.run(debug=True)
#
