from models import db, Message

def new_message(content, role, conversation_id):
    new_message = Message(content=content, role=role, conversation_id=conversation_id)
    db.session.add(new_message)
    db.session.commit()
    return new_message

def get_all_messages():
    return Message.query.all()

def get_messages_in_conversation(conversation_id):
    messages = Message.query.filter_by(conversation_id=conversation_id).all()

    return messages