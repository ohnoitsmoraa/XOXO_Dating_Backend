from flask import Flask, make_response,request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt
from model import *
import os
from dotenv import load_dotenv

# Initialize dotenv
load_dotenv()

# Create Flask application object
app = Flask(__name__)

# Configure database connection to local file
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///dating_site.db')

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

api = Api (app)

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

@jwt.token_in_blocklist_loader
def token_in_blocklist(jwt_header, jwt_data):
    jti = jwt_data['jti']

    token = db.session.query(Token).filter(Token.jti == jti).scalar()

    return token is not None

# Home route
@app.route ('/')
def index():
    return "Welcome to the Dating Site API "

# User routes
@app.route('/users', methods=['GET', 'POST'])
@jwt_required(optional=True) # Allows access without a token for GET requests
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
@jwt_required() # Requires valid JWT token
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
@jwt_required()
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
@jwt_required()
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
@jwt_required()
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
@jwt_required()
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
    
# Restful API
class RegisterUser(Resource):
    def post(self):
        data = request.get_json()
        user = User.get_user_by_username(username=data.get('username'))

        if user is not None:
            return make_response({"error": "Username already exists"}, 400)
        
        new_user = User(username=data.get('username'), email=data.get('email'))
        new_user.set_password(data.get('password'))
        db.session.add(new_user)
        db.session.commit()

        return make_response({"message": "User created successfully"}, 201)

api.add_resource(RegisterUser, '/register')

class LoginUser(Resource):
    def post(self):
        data = request.get_json()
        user = User.get_user_by_username(username=data.get('username'))

        if user is None or not user.check_password(data.get('password')):
            return make_response({"error": "Invalid username or password"}, 401)

        access_token = create_access_token(identity=user.id)
        return make_response({"access_token": access_token}, 200)
    
api.add_resource(LoginUser, '/login')


class LogoutUser(Resource):
    @jwt_required()   # With this you cannot log out without accessing / logging in
    def get(self):
        jwt = get_jwt()
        jti = jwt['jti']

        new_block_list = Token(jti=jti)
        db.session.add(new_block_list)
        db.session.commit()

        return make_response ({"message" : "User logged out successfully"}, 201)


api.add_resource(LogoutUser, '/logout')

class UserResource(Resource):
    # GET method to fetch one or all users
    def get(self, id=None):
        if id:
            user = User.query.get(id)
            if not user:
                return make_response({"error": "User not found"}, 404)
            return make_response(user.to_dict(), 200)
        else:
            users = User.query.all()
            response = [user.to_dict() for user in users]
            return make_response(jsonify(response), 200)
    
    # POST method to create a new user
    def post(self):
        data = request.get_json()
        new_user = User(username=data['username'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return make_response({"message": "User created successfully"}, 201)
    
    # PATCH method to update a user
    def patch(self, id):
        user = User.query.get(id)
        if not user:
            return make_response({"error": "User not found"}, 404)

        data = request.get_json()

        # Update only provided fields
        for attr in data:
            if hasattr(user, attr):
                setattr(user, attr, data[attr])
        
        db.session.commit()
        return make_response(user.to_dict(), 200)

    # DELETE method to delete a user
    def delete(self, id):
        user = User.query.get(id)
        if not user:
            return make_response({"error": "User not found"}, 404)
        
        db.session.delete(user)
        db.session.commit()
        return make_response({"message": "User deleted successfully"}, 200)

api.add_resource(UserResource, '/users', '/users/<int:id>')

class InterestResource(Resource):
    @jwt_required()
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return make_response({"error": "User not found"}, 404)
        interests = [interest.to_dict() for interest in user.interests]
        return make_response(jsonify(interests), 200)

    @jwt_required()
    def post(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return make_response({"error": "User not found"}, 404)

        data = request.get_json()
        new_interest = Interest(name=data['name'], user_id=user_id)
        db.session.add(new_interest)
        db.session.commit()
        return make_response({"message": "Interest added successfully"}, 201)

api.add_resource(InterestResource, '/users/<int:user_id>/interests')

class MatchResource(Resource):
    @jwt_required()
    def get(self):
        matches = Match.query.all()
        response = [match.to_dict() for match in matches]
        return make_response(jsonify(response), 200)

    @jwt_required()
    def post(self):
        data = request.get_json()
        new_match = Match(sender_id=data['sender_id'], receiver_id=data['receiver_id'], 
                          compatibility_score=data['compatibility_score'])
        db.session.add(new_match)
        db.session.commit()
        return make_response({"message": "Match created successfully"}, 201)

api.add_resource(MatchResource, '/matches')

 
if __name__ == '__main__':
     app.run(port=5555, debug=True)