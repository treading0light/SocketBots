import os, hashlib, queue, threading, json
from flask import Flask
from dotenv import load_dotenv
from flask_socketio import SocketIO, emit
from agents import agent_frank

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

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


@socketio.on('connect')
def handle_connect():
    print("Client connected")
    print_thread_status_and_queue_contents()

    # try:


    # except Exception as e:

    


@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

    

# This function handles incoming messages
@socketio.on('user-input')
def handle_user_input(input):
    print("Received message: ", input)
    data = json.loads(input)
    layer_1_queue.put(data)


def send_to_user(in_queue):
    while True:
        message = in_queue.get()
        print(f"sending to user {message}")
        socketio.emit('ai-output', message)

threading.Thread(target=agent_frank, args=(layer_1_queue, output_to_user_queue)).start()
threading.Thread(target=send_to_user, args=(output_to_user_queue,)).start()

if __name__ == '__main__':
    socketio.run(app)