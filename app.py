from flask import Flask, request, render_template
import os
import logging
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static')

def summarize_text(text):
    """Summarize text using Vertex AI Gemini model."""
    try:
        logger.info("Loading Gemini model...")
        model = GenerativeModel("gemini-pro")
        
        # Create the prompt
        prompt = f"""Please summarize the following text concisely:

{text}

Summary:"""
        
        logger.info("Sending request to model...")
        response = model.generate_content(prompt)
        
        logger.info(f"Got response: {response.text}")
        return response.text
    except Exception as e:
        logger.error(f"Error in summarize_text: {str(e)}")
        raise

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form["text"]
        logger.info(f"Received text to summarize: {text[:100]}...")
        try:
            summary = summarize_text(text)
            logger.info(f"Generated summary: {summary}")
            return render_template("index.html", summary=summary, original_text=text)
        except Exception as e:
            error_msg = f"Error generating summary: {str(e)}"
            logger.error(error_msg)
            return render_template("index.html", error=error_msg, original_text=text)
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
