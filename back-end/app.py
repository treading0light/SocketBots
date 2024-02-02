import os, hashlib, queue, threading, json
from flask import Flask
from dotenv import load_dotenv
from flask_socketio import SocketIO, emit
from controllers.message_controller import new_message, get_messages_in_conversation
from controllers.conversation_controller import new_conversation, get_all_conversations
from models import db
from agents import agent_frank

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
socketio = SocketIO(app, cors_allowed_origins="*")

with app.app_context():
    db.create_all()

layer_1_queue = queue.Queue()
output_to_user_queue = queue.Queue()

def print_thread_status_and_queue_contents():
    # Print thread status
    for thread in threading.enumerate():
        print(f"Thread Name: {thread.name}, Alive: {thread.is_alive()}")

    # Print queue contents (assuming you have a list of queues)
    queues = [layer_1_queue, output_to_user_queue]  # Add all your queues to this list
    for i, q in enumerate(queues, start=1):
        queue_status = "empty" if q.empty() else "not empty"
        print(f"Queue {i} is {queue_status}")

@socketio.on('get-conversations')
def get_conversations():
    conversations = get_all_conversations()
    return conversations

@socketio.on('get-messages')
def get_messages(conversation_id):
    messages = get_messages_in_conversation(conversation_id)
    return messages

@socketio.on('connect')
def handle_connect():
    print("Client connected")
    print_thread_status_and_queue_contents()


@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

    

# This function handles incoming messages
@socketio.on('user-input')
def handle_user_input(input, conversation_id):
    print("Received message: ", input)
    message = new_message(input, "user", conversation_id)
    layer_1_queue.put(message)

@socketio.on('new-conversation')
def handle_new_conversation():
    conversation = new_conversation()
    return conversation

def send_to_user(in_queue):
    while True:
        message = in_queue.get()
        print(f"sending to user {message}")
        socketio.emit('ai-output', message)

threading.Thread(target=agent_frank, args=(layer_1_queue, output_to_user_queue)).start()
threading.Thread(target=send_to_user, args=(output_to_user_queue,)).start()

if __name__ == '__main__':
    socketio.run(app)