import queue, threading
from flask import Flask
from flask_socketio import SocketIO
from controllers.message_controller import new_message, get_messages_in_conversation
from controllers.conversation_controller import new_conversation, get_all_conversations, delete_conversation, update_last_opened
from tools import MainChatTools as tools
from models import db
from agents import SoloAgents
from crews import NamingCrew

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
socketio = SocketIO(app, cors_allowed_origins="*")

with app.app_context():
    db.create_all()

layer_1_queue = queue.Queue()
output_to_user_queue = queue.Queue()
background_tasks_queue = queue.Queue()
crew_queue = queue.Queue()
tool_call_queue = queue.Queue()

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
    print("Conversations: ", conversations)
    return conversations

@socketio.on('new-conversation')
def handle_new_conversation():
    conversation = new_conversation()
    print("New conversation created: ", conversation)
    return conversation

@socketio.on('delete-conversation')
def handle_delete_conversation(conversation_id):
    print("Deleting conversation: ", conversation_id)
    delete_conversation(conversation_id)
    return 'Conversation deleted successfully'

@socketio.on('get-messages')
def get_messages(conversation_id):
    messages = get_messages_in_conversation(conversation_id)
    update_last_opened(conversation_id)
    return messages

@socketio.on('connect')
def handle_connect():
    print("Client connected")
    # print_thread_status_and_queue_contents()


@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

@socketio.on('request-rename')
def handle_request_rename(conversation_id):
    messages = get_messages_in_conversation(conversation_id)
    naming_crew = NamingCrew(messages, conversation_id)
    crew_queue.put((naming_crew, conversation_id))

@socketio.on('user-input')
def handle_user_input(data):
    check_threads()
    messages = data.get('messages')
    conversation_id = data.get('conversation_id')
    user_message = data.get('user_message')
    
    message = new_message(**user_message)
    messages.append(message)
    layer_1_queue.put((messages, conversation_id))
    
    return message

def send_to_user(in_queue, tool_call_queue, app):
    while True:
        raw_message, convo_id = in_queue.get()
        with app.app_context():
            message = new_message(raw_message.content, raw_message.role, convo_id)
        if "[TOOL_CALL]" in message['content'] and "[/TOOL_CALL]" in message['content']:
            tool_call_queue.put((message, convo_id))
        
        if len(message['content']) > 0:
            print(f"sending to user {message}")
            socketio.emit('ai-output', message)

def check_threads():
    for thread in threading.enumerate():
        if not thread.is_alive():
            print("Thread is dead")
            thread.start()

def delegate_to_crew(in_queue, out_queue):
    while True:
        crew, convo_id = in_queue.get()
        result = crew.run()
        out_queue.put((result, convo_id))


threads = [
    threading.Thread(target=SoloAgents.agent_frank, args=(layer_1_queue, output_to_user_queue)).start(),
    threading.Thread(target=tools.make_tool_call, args=(tool_call_queue, output_to_user_queue)).start(),
    threading.Thread(target=send_to_user, args=(output_to_user_queue, tool_call_queue, app)).start(),
    threading.Thread(target=delegate_to_crew, args=(crew_queue, output_to_user_queue)).start()
]

if __name__ == '__main__':
    socketio.run(app)