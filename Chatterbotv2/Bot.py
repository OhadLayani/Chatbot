from chatterbot import ChatBot
from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import json
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# To prevent errors related to time.clock in Python 3.8+
time.clock = time.time

# Create a new ChatBot instance with the SQLite storage adapter
chatbot = ChatBot(
    'MyBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///my_bot_database.sqlite3'  # Using the existing SQLite database
)

# Path to the file that will store the chat history
history_file = 'chat_history.json'

# Load chat history from file
def load_chat_history():
    if os.path.exists(history_file):
        with open(history_file, 'r') as file:
            return json.load(file)
    return []

# Save chat history to file
def save_chat_history():
    with open(history_file, 'w') as file:
        json.dump(chat_history, file)

# Initialize chat history (load from file)
chat_history = load_chat_history()

# Define an endpoint for chatting
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message")

    # Get response from chatbot
    bot_response = chatbot.get_response(user_message)

    # Append to chat history
    chat_history.append({
        'user': user_message,
        'bot': str(bot_response)
    })

    # Save updated chat history to file
    save_chat_history()

    # Return response in JSON format
    return jsonify({'response': str(bot_response)})

# Define an endpoint to get chat history
@app.route('/history', methods=['GET'])
def history():
    return jsonify(chat_history)

if __name__ == '__main__':
    app.run(port=5000, debug=True)