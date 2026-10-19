
from flask import Flask, request, jsonify
from flask_cors import CORS

from final import answer_question

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Please enter a question."}), 400

    try:
        answer = answer_question(question)
        return jsonify({"answer": answer})
    except Exception:
        app.logger.exception("Chat request failed")
        return jsonify({"error": "Unable to generate an answer."}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
