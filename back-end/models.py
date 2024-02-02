from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    role = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=False)
    conversation = db.relationship('Conversation', backref=db.backref('messages', lazy=True))

    def __repr__(self):
        return f'<Message {self.id}>'
    
class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f'<Conversation {self.id}>'