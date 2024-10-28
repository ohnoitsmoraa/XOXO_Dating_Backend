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
        # Creating users
        users = [
            User(username="JaneDoe", email="jane@example.com", bio="Love to travel, cook, and meet new people. Always up for an adventure!"),
            User(username="JohnSmith", email="john@example.com", bio="Avid reader, tech enthusiast, and runner. Always chasing the next big idea."),
            User(username="EmilyJohnson", email="emily@example.com", bio="Fashion designer who loves painting and outdoor activities. Always exploring creativity!"),
            User(username="MichaelBrown", email="michael@example.com", bio="Entrepreneur and foodie. Can’t say no to a good book or a culinary adventure!"),
            User(username="SophiaWilliams", email="sophia@example.com", bio="Yoga instructor with a passion for wellness and meditation. Loves to be outdoors."),
            User(username="JamesMiller", email="james@example.com", bio="Software engineer with a love for gaming and sci-fi. Always coding something cool!"),
            User(username="OliviaDavis", email="olivia@example.com", bio="Photographer capturing moments of life. Love hiking and exploring new landscapes."),
            User(username="DavidWilson", email="david@example.com", bio="Guitarist in a band and music lover. Can’t live without tunes and adventures!"),
            User(username="EmmaClark", email="emma@example.com", bio="Digital marketer with a love for travel and food. Enjoys good company and good vibes."),
            User(username="ChrisEvans", email="chris@example.com", bio="Fitness coach and mountain climber. Always chasing new challenges."),
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
            Token(jti="token_for_jane_doe"),
            Token(jti="token_for_sophia_williams"),
            Token(jti="token_for_david_wilson")
        ]

        db.session.add_all(tokens)
        db.session.commit()

        print("Seeding done!")
    
    except Exception as e:
        print(f"An error occurred during seeding: {e}")
        db.session.rollback()
