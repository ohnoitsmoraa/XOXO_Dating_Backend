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

if __name__ == '__main__':
     app.run(port=8080, debug=True)