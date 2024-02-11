from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect
import datetime

db = SQLAlchemy()


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    role = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id', ondelete='CASCADE'), nullable=False)

    def to_dict(self):
        """Convert a SQLAlchemy model instance into a dictionary without relationships."""
        return {
            "content": self.content,
            "role": self.role,
        }
    
class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    last_opened = db.Column(db.DateTime, server_default=db.func.now())
    messages = db.relationship('Message', backref='conversation', cascade="all, delete-orphan")

    def to_dict(self):
        """Convert a SQLAlchemy model instance into a dictionary."""
        instance_dict = {
            "name": self.name,
            "id": self.id
        }

        if self.messages:
            instance_dict["messages"] = [message.to_dict() for message in self.messages]
        else:
            instance_dict["messages"] = []

        # for attr in inspect(self).attrs:
        #     value = getattr(self, attr.key)
        #     if isinstance(value, datetime.datetime):
        #         instance_dict[attr.key] = value.isoformat()
        #     elif isinstance(value, list):
        #         instance_dict[attr.key] = [item.to_dict() for item in value]
        #     else:
        #         instance_dict[attr.key] = value
        return instance_dict