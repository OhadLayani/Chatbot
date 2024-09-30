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

# Folder to store the chat histories of different sessions
history_folder = 'chat_histories'

# Ensure the folder exists
if not os.path.exists(history_folder):
    os.makedirs(history_folder)

# Load chat history for a specific session
def load_chat_history(session_id):
    history_file = os.path.join(history_folder, f'{session_id}.json')
    if os.path.exists(history_file):
        with open(history_file, 'r') as file:
            return json.load(file)
    return []

# Save chat history for a specific session
def save_chat_history(session_id, chat_history):
    history_file = os.path.join(history_folder, f'{session_id}.json')
    with open(history_file, 'w') as file:
        json.dump(chat_history, file)

# Define an endpoint for chatting
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message")
    session_id = data.get("session_id")  # Get session_id from the request

    # Load the session-specific chat history
    chat_history = load_chat_history(session_id)

    # Get response from chatbot
    bot_response = chatbot.get_response(user_message)

    # Append to chat history
    chat_history.append({
        'user': user_message,
        'bot': str(bot_response)
    })

    # Save updated chat history to file
    save_chat_history(session_id, chat_history)

    # Return response in JSON format
    return jsonify({'response': str(bot_response)})

# Define an endpoint to get chat history for a specific session
@app.route('/history', methods=['GET'])
def history():
    session_id = request.args.get('session_id')  # Get session_id from the query params
    chat_history = load_chat_history(session_id)
    return jsonify(chat_history)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
