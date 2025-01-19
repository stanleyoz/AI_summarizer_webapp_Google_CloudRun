from flask import Flask, request, render_template

from transformers import pipeline

import os

app = Flask(__name__)

# Initialize the model with error handling

try:

    summarizer = pipeline("summarization")

except Exception as e:

    print(f"Error loading model: {e}")

    summarizer = None

@app.route("/", methods=["GET", "POST"])

def index():

    if request.method == "POST":

        text = request.form["text"]

        if summarizer:

            try:

                summary = summarizer(text, max_length=150, min_length=30, do_sample=False)

                return render_template("index.html", summary=summary[0]["summary_text"], original_text=text)

            except Exception as e:

                return render_template("index.html", error=str(e), original_text=text)

        else:

            return render_template("index.html", error="Summarizer not initialized", original_text=text)

    return render_template("index.html")

if name == "__main__":

    port = int(os.getenv("PORT", 8080))

    app.run(debug=False, host="0.0.0.0", port=port)
