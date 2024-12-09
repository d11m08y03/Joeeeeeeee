import requests
from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from database import db
from models.conversation import Conversation

OLLAMA_BASE_URL = "http://localhost:11434/api/generate"  # Local Ollama API endpoint

chat_blueprint = Blueprint("chat", __name__, template_folder="../views")


@chat_blueprint.route("/")
@login_required
def index():
    conversations = Conversation.query.filter_by(user_id=current_user.id).all()
    return render_template("index.html", conversations=conversations)


@chat_blueprint.route("/api/chat", methods=["POST"])
@login_required
def chat():
    data = request.json

    # Ensure the prompt is provided in the request
    if not data or "prompt" not in data:
        return jsonify({"error": "Prompt is required"}), 400

    prompt = data["prompt"]

    # Prepare the request payload for Ollama
    payload = {
        "model": "qwen:0.5b",
        "prompt": prompt,
        "stream": False,
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(OLLAMA_BASE_URL, headers=headers, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({
            "error": f"Failed to communicate with Ollama API: {str(e)}"
        }), 500

    # Process the response from Ollama
    result = response.json()
    response_text = result.get("response", "")

    if not response_text:
        return jsonify({"error": "Ollama API returned an empty response"}), 500

    # Save the conversation to the database
    conversation = Conversation(
        user_id=current_user.id, prompt=prompt, response=response_text
    )
    db.session.add(conversation)
    db.session.commit()

    return jsonify({"response": response_text})
