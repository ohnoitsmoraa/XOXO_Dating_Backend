from flask import Flask, make_response,request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, jwt_optional
from models import *
import os
from dotenv import load_dotenv

# Initialize dotenv
load_dotenv()

# Create Flask application object
app = Flask(__name__)

# Configure database connection to local file
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')

# Disable modification tracking 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure JWT SECRET KEY  
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

# Create a Migrate object to manage schema modifications
migrate = Migrate(app, db)

# Initialized the Flask app
db.init_app(app)

# Initializing JWT
jwt = JWTManager(app)

# Error handlers for JWT
@jwt.unauthorized_loader
def unauthorized_response(error):
    return make_response({"error": "Missing authorization header"}, 401)

@jwt.invalid_token_loader
def invalid_token_response(error):
    return make_response({"error": "Invalid token"}, 401)

@jwt.expired_token_loader
def expired_token_response(expired_token):
    return make_response({"error": "Token has expired"}, 401)

# Home route
@app.route ('/')
def index():
    return "Welcome to the Dating Site API "

# User routes
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
    if 'username' in data:
            user.username = data['username']
    if 'email' in data:
            user.email = data['email']
        
    db.session.commit()
    return make_response(user.to_dict(), 200)

# Interest route
@app.route('/users/<int:user_id>/interests', methods=['GET', 'POST'])
def user_interests(user_id):
    user = User.query.get(user_id)

    if request.method == 'GET':
        if not user:
            return make_response({"error": "User not found"}, 404)
        interests = [interest.to_dict() for interest in user.interests]
        return make_response(jsonify(interests), 200)

    if request.method == 'POST':
        if not user:
            return make_response({"error": "User not found"}, 404)
        
        data = request.get_json()
        new_interest = Interest(name=data['name'], user_id=user_id)
        db.session.add(new_interest)
        db.session.commit()
        return make_response({"message": "Interest added successfully"}, 201)

@app.route('/interests/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def interest(id):
    interest = Interest.query.get(id)

    if request.method == 'GET':
        if not interest:
            return make_response({"error": "Interest not found"}, 404)
        return make_response(interest.to_dict(), 200)

    if request.method == 'PATCH':
        if not interest:
            return make_response({"error": "Interest not found"}, 404)
        
        data = request.get_json()
        if 'name' in data:
            interest.name = data['name']
        
        db.session.commit()
        return make_response(interest.to_dict(), 200)

    if request.method == 'DELETE':
        if not interest:
            return make_response({"error": "Interest not found"}, 404)

        db.session.delete(interest)
        db.session.commit()
        return make_response({"message": "Interest deleted successfully"}, 200)
    
# Match route
@app.route('/matches', methods=['GET', 'POST'])
def matches():
    if request.method == 'GET':
        matches = Match.query.all()
        response = [match.to_dict() for match in matches]
        return make_response(jsonify(response), 200)

    if request.method == 'POST':
        data = request.get_json()
        new_match = Match(sender_id=data['sender_id'], receiver_id=data['receiver_id'], 
                          compatibility_score=data['compatibility_score'])
        db.session.add(new_match)
        db.session.commit()
        return make_response({"message": "Match created successfully"}, 201)

@app.route('/matches/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def match(id):
    match = Match.query.get(id)

    if request.method == 'GET':
        if not match:
            return make_response({"error": "Match not found"}, 404)
        return make_response(match.to_dict(), 200)

    if request.method == 'PATCH':
        if not match:
            return make_response({"error": "Match not found"}, 404)
        
        data = request.get_json()
        if 'status' in data:
            match.status = data['status']
        if 'compatibility_score' in data:
            match.compatibility_score = data['compatibility_score']
        
        db.session.commit()
        return make_response(match.to_dict(), 200)

    if request.method == 'DELETE':
        if not match:
            return make_response({"error": "Match not found"}, 404)

        db.session.delete(match)
        db.session.commit()
        return make_response({"message": "Match deleted successfully"}, 200)

 
if __name__ == '__main__':
     app.run(port=5555, debug=True)