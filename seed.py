#!/usr/bin/env python3

from app import app
from model import *
from werkzeug.security import generate_password_hash

with app.app_context():
    try:
        # Clear out existing data to avoid having duplicate entries in your database
        print("Deleting data...")
        db.session.query(Token).delete()
        db.session.query(Interest).delete()
        db.session.query(Match).delete()
        db.session.query(User).delete()
        db.session.commit()

        print("Creating users...")
        # Creating users with profile pictures and hashed passwords
        users = [
            User(username="JaneDoe", email="jane@example.com", password=generate_password_hash("password123"), bio="Love to travel, cook, and meet new people.",
                 profile_picture="https://randomuser.me/api/portraits/women/44.jpg"),
            User(username="JohnSmith", email="john@example.com", password=generate_password_hash("password123"), bio="Avid reader, tech enthusiast, and runner.",
                 profile_picture="https://randomuser.me/api/portraits/men/45.jpg"),
            User(username="EmilyJohnson", email="emily@example.com", password=generate_password_hash("password123"), bio="Fashion designer who loves painting.",
                 profile_picture="https://randomuser.me/api/portraits/women/46.jpg"),
            User(username="MichaelBrown", email="michael@example.com", password=generate_password_hash("password123"), bio="Entrepreneur and foodie.",
                 profile_picture="https://randomuser.me/api/portraits/men/46.jpg"),
            User(username="SophiaWilliams", email="sophia@example.com", password=generate_password_hash("password123"), bio="Yoga instructor with a passion for wellness.",
                 profile_picture="https://randomuser.me/api/portraits/women/47.jpg"),
            User(username="JamesMiller", email="james@example.com", password=generate_password_hash("password123"), bio="Software engineer with a love for gaming.",
                 profile_picture="https://randomuser.me/api/portraits/men/47.jpg"),
            User(username="OliviaDavis", email="olivia@example.com", password=generate_password_hash("password123"), bio="Photographer capturing moments of life.",
                 profile_picture="https://randomuser.me/api/portraits/women/48.jpg"),
            User(username="DavidWilson", email="david@example.com", password=generate_password_hash("password123"), bio="Guitarist in a band and music lover.",
                 profile_picture="https://randomuser.me/api/portraits/men/48.jpg"),
            User(username="EmmaClark", email="emma@example.com", password=generate_password_hash("password123"), bio="Digital marketer with a love for travel.",
                 profile_picture="https://randomuser.me/api/portraits/women/49.jpg"),
            User(username="ChrisEvans", email="chris@example.com", password=generate_password_hash("password123"), bio="Fitness coach and mountain climber.",
                 profile_picture="https://randomuser.me/api/portraits/men/49.jpg"),
        ]

        db.session.add_all(users)
        db.session.commit()

        # Retrieve user IDs for further associations
        user_dict = {user.username: user.id for user in users}

        print("Creating interests...")
        # Creating interests
        interests = [
            Interest(name="hiking", user_id=user_dict["JaneDoe"]),
            Interest(name="cooking", user_id=user_dict["JohnSmith"]),
            Interest(name="gaming", user_id=user_dict["EmilyJohnson"]),
            Interest(name="reading", user_id=user_dict["MichaelBrown"]),
            Interest(name="traveling", user_id=user_dict["SophiaWilliams"]),
            Interest(name="cycling", user_id=user_dict["JamesMiller"]),
            Interest(name="swimming", user_id=user_dict["OliviaDavis"]),
            Interest(name="playing golf", user_id=user_dict["DavidWilson"]),
            Interest(name="crotcheting", user_id=user_dict["EmmaClark"]),
            Interest(name="knitting", user_id=user_dict["ChrisEvans"]),
        ]

        db.session.add_all(interests)
        db.session.commit()

        print("Creating matches...")
        # Creating matches
        matches = [
            Match(sender_id=user_dict["JaneDoe"], receiver_id=user_dict["EmilyJohnson"], status="accepted", compatibility_score=85.0),
            Match(sender_id=user_dict["MichaelBrown"], receiver_id=user_dict["OliviaDavis"], status="pending", compatibility_score=75.0),
            Match(sender_id=user_dict["SophiaWilliams"], receiver_id=user_dict["DavidWilson"], status="rejected", compatibility_score=60.0),
        ]

        db.session.add_all(matches)
        db.session.commit()

        print("Creating tokens...")
        # Creating tokens
        tokens = [
            Token(jti="token_for_jane_doe", user_id=user_dict["JaneDoe"]),
            Token(jti="token_for_sophia_williams", user_id=user_dict["SophiaWilliams"]),
            Token(jti="token_for_david_wilson", user_id=user_dict["DavidWilson"]),
        ]

        db.session.add_all(tokens)
        db.session.commit()

        print("Seeding done!")

    except Exception as e:
        print(f"An error occurred during seeding: {e}")
        db.session.rollback()
