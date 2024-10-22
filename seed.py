#!/usr/bin/env python3

from app import app
from model import *
from werkzeug.security import generate_password_hash

with app.app_context():
    # Clear out existing data to avoid having duplicate entries in your database
    print("Deleting data...")
    db.session.query(Token).delete()
    db.session.query(Interest).delete()
    db.session.query(Match).delete()
    db.session.query(User).delete()
    db.session.commit()

    print("Creating users.....................")
    chelsey = User(username="Kamren", email="kamrenbae@gmail.com", bio="I love nature walks")
    chelsey.set_password("pass123")
    patricia = User(username="Karianne", email="kari@gmail.com", bio="Dancing is bae")
    patricia.set_password("pat_on_my_shoulder")
    nicholas = User(username="Maxime_Nienow", email="max001@gmail.com", bio="Video gaming")
    nicholas.set_password("nichie")
    clement = User(username="Sam", email="samhacker@gmail.com", bio="# Fanfiction")
    clement.set_password("cele@254")
    ervin = User(username="Antonette", email="antonita@gmail.com", bio="Travelling")
    ervin.set_password("erilove")
    glenn = User(username="phine", email="phin@gmail.com", bio="Ride or die")
    glenn.set_password("lenny_bro")
    leanne = User(username="Bret", email="bret354@gmail.com", bio="You swimming through my mind")
    leanne.set_password("anne_loves_her")
    max = User(username="Moriah.Stanton", email="stanton@gmail.com", bio="Love hittin' balls")
    max.set_password("maxie")
    dennis = User(username="Leopoldo_Corkery", email="leo006@gmail.com", bio="Crotcheting")
    dennis.set_password("dennie")
    kurtis = User(username="Elwyn.Skiles", email="ski@gmail.com", bio="Knitting all the way")
    kurtis.set_password("playboi_karti")

    db.session.add_all([chelsey, patricia, nicholas, clement, ervin, glenn, leanne, max, dennis, kurtis])
    db.session.commit()

    print("Creating interests................")
    i1 = Interest(name="Hiking", user_id=chelsey.id)
    i2 = Interest(name="Cooking", user_id=patricia.id)
    i3 = Interest(name="Gaming", user_id=nicholas.id)
    i4 = Interest(name="Reading", user_id=clement.id)
    i5 = Interest(name="Travelling", user_id=ervin.id)
    i6 = Interest(name="Cycling", user_id=glenn.id)
    i7 = Interest(name="Swimming", user_id=leanne.id)
    i8 = Interest(name="Playing golf", user_id=max.id)
    i9 = Interest(name="Crotcheting", user_id=dennis.id)
    i10 = Interest(name="Knitting", user_id=kurtis.id)

    db.session.add_all([i1, i2, i3, i4, i5, i6, i7, i8, i9, i10])
    db.session.commit()

    print("Creating matches.................")
    m1 = Match(sender_id=chelsey.id, receiver_id=nicholas.id, status="accepted", compatibility_score=85.0)
    m2 = Match(sender_id=clement.id, receiver_id=leanne.id, status="pending", compatibility_score=75.0)
    m3 = Match(sender_id=ervin.id, receiver_id=max.id, status="rejected", compatibility_score=60.0)

    db.session.add_all([m1, m2, m3])
    db.session.commit()

    print("Creating tokens..................")
    token1 = Token(jti="token_for_chelsey")
    token2 = Token(jti="token_for_ervin")
    token3 = Token(jti="token_for_max")

    db.session.add_all([token1, token2, token3])
    db.session.commit()

    print("Seeding done!")
