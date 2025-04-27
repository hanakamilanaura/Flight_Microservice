from flask import Flask, jsonify, request, render_template
from models import db, User
from werkzeug.security import generate_password_hash
import requests

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost:5432/user_service_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/user')
def user_service():
    users = User.query.all()
    return render_template('user.html', users=users)

@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    hashed_password = generate_password_hash(data['password'])
    
    new_user = User(
        name=data['name'],
        email=data['email'],
        password=hashed_password
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify(new_user.to_dict()), 201

# Provider Endpoints
@app.route('/api/users/validate', methods=['POST'])
def validate_user():
    data = request.json
    user_id = data.get('user_id')
    if User.query.get(user_id):
        return jsonify({'status': 'success', 'valid': True}), 200
    return jsonify({'status': 'error', 'valid': False}), 404

# Consumer Endpoints
@app.route('/api/users/<int:user_id>/bookings', methods=['GET'])
def get_user_bookings(user_id):
    # Consumer: Get bookings from Booking Service
    try:
        response = requests.get(f'http://booking-service:5002/api/bookings/user/{user_id}')
        return jsonify(response.json()), response.status_code
    except requests.RequestException as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)