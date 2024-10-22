#!/usr/bin/env python3

from app import app
from models import db, User, Match, Message
from datetime import datetime

with app.app_context():
    # Clear out existing data to avoid having duplicate entries in your database
    print("Deleting data...")
    Message.query.delete()
    Match.query.delete()
    User.query.delete()

    print("Creating users...")
    alice = User(username="Alice", email="alice@example.com", bio="I love hiking and reading")
    bob = User(username="Bob", email="bob@example.com", bio="Passionate about cooking and travel")
    charlie = User(username="Charlie", email="charlie@example.com", bio="Tech enthusiast and gamer")
    users = [alice, bob, charlie]

    print("Creating matches...")
    match1 = Match(user1=alice, user2=bob, status="accepted")
    match2 = Match(user1=bob, user2=charlie, status="pending")
    match3 = Match(user1=charlie, user2=alice, status="rejected")
    matches = [match1, match2, match3]

    print("Creating messages...")
    message1 = Message(sender=alice, receiver=bob, content="Hi Bob! I liked your profile.")
    message2 = Message(sender=bob, receiver=alice, content="Thanks Alice! I'd love to chat more.")
    message3 = Message(sender=bob, receiver=charlie, content="Hey Charlie, want to meet up?")
    messages = [message1, message2, message3]

    db.session.add_all(users)
    db.session.add_all(matches)
    db.session.add_all(messages)
    db.session.commit()

    print("Seeding done!")