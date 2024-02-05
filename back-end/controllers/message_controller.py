from models import db, Message

def new_message(content, role, conversation_id):
    new_message = Message(content=content, role=role, conversation_id=conversation_id)
    db.session.add(new_message)
    db.session.commit()
    print("New message created: ", new_message.to_dict())
    return new_message.to_dict()

def get_all_messages():
    messages = Message.query.all()
    return [message.to_dict() for message in messages]

def get_messages_in_conversation(conversation_id):
    messages = Message.query.filter_by(conversation_id=conversation_id).all()

    return [message.to_dict() for message in messages]