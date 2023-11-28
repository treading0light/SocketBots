import os, hashlib
from supabase import create_client, Client
from dotenv import load_dotenv
from flask_socketio import SocketIO, emit
from flask import Flask

app = Flask(__name__)
socketio = SocketIO(app)


load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
database: Client = create_client(url, key)
auth = database


@socketio.on('connect')
def handle_connect():
    print("Client connected")

    # try:

    # except Exception as e:

    


@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

    

# This function handles incoming messages
@socketio.on('message')
def handle_message(message):
    print("Received message: ", message)
    # Logic for processing the received message
    emit('response', {'data': 'Message received!'})

def user_login(email: str, password: str):
    try:
        res = supabase.auth.sign_in_with_password({
        "email": email,
        "password": hash_password(password),
        })

        print(res)
    except Exception as e:
        pass
def user_signup(email: str, password: str):
    try:
        res = supabase.auth.sign_up({
        "email": email,
        "password": hash_password(password),
        })

        print(res)
    except Exception as e:
        pass

def hash_password(password):
   password_bytes = password.encode('utf-8')

   hash_object = hashlib.sha256(password_bytes)

   return hash_object.hexdigest()

if __name__ == '__main__':
    socketio.run(app)