from models import db, Message

def new_conversation():
    conversation = Conversation(name="...")
    db.session.add(conversation)
    db.session.commit()
    return conversation

def get_all_conversations():
    return Conversation.query.all()

def rename_conversation(conversation_id, new_name):
    conversation = Conversation.query.get(conversation_id)
    conversation.name = new_name
    db.session.commit()
    return conversation