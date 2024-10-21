from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone


db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    _tablename_ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    bio = db.Column(db.Text)
    password = db.Column(db.String(50))
    interests = db.relationship('Interest', back_populates='user', cascade='all, delete-orphan')
    sent_matches = db.relationship('Match', foreign_keys='Match.sender_id', back_populates='sender')
    received_matches = db.relationship('Match', foreign_keys='Match.receiver_id', back_populates='receiver')

    serialize_rules = ('-interests.user', '-sent_matches.sender', '-received_matches.receiver')

    @validates('email')
    def validate_email(self, key, email):
        if '@' not in email:
            raise ValueError("Invalid email format")
        return email
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    @classmethod
    def get_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

class Interest(db.Model, SerializerMixin):
    _tablename_ = 'interests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='interests')

    serialize_rules = ('-user',)

class Match(db.Model, SerializerMixin):
    _tablename_ = 'matches'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'accepted', 'rejected'
    compatibility_score = db.Column(db.Float)  # User submittable attribute

    sender = db.relationship('User', foreign_keys=[sender_id], back_populates='sent_matches')
    receiver = db.relationship('User', foreign_keys=[receiver_id], back_populates='received_matches')

    serialize_rules = ('-sender.sent_matches', '-receiver.received_matches')

    @validates('status')
    def validate_status(self, key, status):
        valid_statuses = ['pending', 'accepted', 'rejected']
        if status not in valid_statuses:
            raise ValueError("Invalid status")
        return status

    @validates('compatibility_score')
    def validate_compatibility_score(self, key, score):
        if not 0 <= score <= 100:
            raise ValueError("Compatibility score must be between 0 and 100")
        return score
    
class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column (db.String(255), nullable=False, index=True)
    created_at = db.Column (db.DateTime, default=datetime.now(timezone.utc))