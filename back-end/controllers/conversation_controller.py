from models import db, Conversation

def new_conversation():
    conversation = Conversation(name="...")
    db.session.add(conversation)
    db.session.commit()
    return conversation

def get_all_conversations():
    conversations = Conversation.query.all()
    if not conversations:
        new_convo = new_conversation()
        return [new_convo]
    return conversations

def rename_conversation(conversation_id, new_name):
    conversation = Conversation.query.get(conversation_id)
    conversation.name = new_name
    db.session.commit()
    return conversation