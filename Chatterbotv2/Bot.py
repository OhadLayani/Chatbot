from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import time
import nltk
nltk.download('punkt_tab')
time.clock = time.time
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# To prevent errors related to time.clock in Python 3.8+
time.clock = time.time

# Create a new ChatBot instance with the SQLite storage adapter
chatbot = ChatBot(
    'MyBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///my_bot_database.sqlite3'  # Using the existing SQLite database
)

# Now the chatbot is ready to use without retraining
#while True:
#    user_input = input("You: ")
 #   if user_input.lower() == 'exit':
  #      break
   # response = chatbot.get_response(user_input)
    #print("Bot:", response)
# Define an endpoint for chatting
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message")

    # Get response from chatbot
    bot_response = chatbot.get_response(user_message)

    # Return response in JSON format
    return jsonify({'response': str(bot_response)})


if __name__ == '__main__':
    app.run(port=5000, debug=True)