from flask import Flask, render_template, request, jsonify
from util import load_faq, ChatEngine, correct_spelling

app = Flask(__name__)

# Load FAQ
questions, answers = load_faq("faq_data.json")
engine = ChatEngine(questions)

greetings = ["hi", "hello", "hey"]

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"].lower()

    if any(greet in user_input for greet in greetings):
        return jsonify({"response": "Hello! 😊"})

    corrected = correct_spelling(user_input, questions)
    response = engine.get_response(corrected, questions, answers)

    if response:
        return jsonify({"response": response})
    else:
        return jsonify({"response": "Sorry, I couldn't understand that."})


from waitress import serve
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    serve(app, host="0.0.0.0", port=port)