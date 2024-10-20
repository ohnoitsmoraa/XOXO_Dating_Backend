from flask import Flask, make_response,request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import *

# Create Flask application object
app = Flask(__name__)

# Configure database connection to local file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dating_site.db'

# Disable modification tracking 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create a Migrate object to manage schema modifications
migrate = Migrate(app, db)

# Initialized the Flask app
db.init_app(app)

# Routes
@app.route ('/')
def index():
    return "Welcome to Flask Application"

@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        users = User.query.all()
        response = [user.to_dict() for user in users] 
        return make_response(jsonify(response), 200)

    if request.method == 'POST':
        data = request.get_json()
        new_user = User(username=data['username'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return make_response({"message": "Success"}, 201) 

@app.route('/users/<int:id>', methods=['GET', 'PATCH', 'DELETE']) 
def user(id):
    if request.method == 'GET':
        user = User.query.get(id)

        if not user:
            return make_response({"error": "User not found"}, 404)
        
        return make_response(user.to_dict(), 200)
    
    if request.method == 'DELETE':
        user = User.query.get(id)

        if not user:
            return make_response({"error": "User not found"}, 404)

        db.session.delete(user)
        db.session.commit()
        return make_response({"message": "Success"}, 200)
    
    if request.method == 'PATCH':
        user = User.query.get(id)
        data = request.get_json()

        if not user:
            return make_response({"error": "User not found"}, 404)

        user.username = data['username']
        user.email = data['email']
        db.session.commit()
        return make_response(user.to_dict(), 200)
    
    data = request.get_json()
    print(data)
    for attr in data:
        setattr(user, attr, data[attr])
        db.session.commit()
        return make_response(user.to_dict(), 200)


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    posts = Post.query.all()
    response = [post.to_dict() for post in posts]
    return make_response(response, 200)