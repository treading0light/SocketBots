from models import db, Conversation
from sqlalchemy.orm import load_only

def new_conversation():
    
    conversation = Conversation(name="...")
    db.session.add(conversation)
    db.session.commit()
    return conversation.to_dict()

def get_all_conversations():
    conversations = Conversation.query.order_by(Conversation.last_opened).all()
    if not conversations:
        new_convo = new_conversation()
        return [new_convo]
    
    if len(conversations) > 10: 
        # delete the oldest 5 conversations
        for i in range(len(conversations) - 5):
            db.session.delete(conversations[i])
        db.session.commit()
    
    # for convo in conversations:
    #     convo.message = [message.to_dict() for message in convo.messages]
    return [conversation.to_dict() for conversation in conversations]

def rename_conversation(conversation_id, new_name):
    conversation = Conversation.query.get(conversation_id)
    conversation.name = new_name
    db.session.commit()
    print("Conversation renamed: ", conversation.to_dict())
    return conversation.to_dict()

def delete_conversation(conversation_id):
    conversation = Conversation.query.get(conversation_id)
    db.session.delete(conversation)
    db.session.commit()

def update_last_opened(conversation_id):
    conversation = Conversation.query.get(conversation_id)
    conversation.last_opened = db.func.now()
    db.session.commit()
    return conversation.to_dict()