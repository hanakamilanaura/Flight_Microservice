from flask import Flask, jsonify, request, render_template
from models import db, Booking
import requests
from datetime import datetime
import uuid

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost:5432/booking_service_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/booking')
def booking_service():
    bookings = Booking.query.all()
    # Fetch additional data from other services
    enriched_bookings = []
    
    for booking in bookings:
        # Get user details
        user_response = requests.get(f'http://localhost:5000/api/users/{booking.user_id}')
        user_data = user_response.json() if user_response.ok else None
        
        # Get flight details
        flight_response = requests.get(f'http://localhost:5001/api/flights/{booking.flight_code}')
        flight_data = flight_response.json() if flight_response.ok else None
        
        booking_data = booking.to_dict()
        if user_data:
            booking_data['user_name'] = user_data['name']
        if flight_data:
            booking_data['from'] = flight_data['from']
            booking_data['to'] = flight_data['to']
            
        enriched_bookings.append(booking_data)
    
    return render_template('booking.html', bookings=enriched_bookings)

@app.route('/api/bookings', methods=['POST'])
def create_booking():
    data = request.json
    
    # Validate user
    user_response = requests.get(f'http://localhost:5000/api/users/{data["user_id"]}')
    if not user_response.ok:
        return jsonify({'error': 'Invalid user'}), 400
        
    # Validate flight
    flight_response = requests.get(f'http://localhost:5001/api/flights/{data["flight_code"]}')
    if not flight_response.ok:
        return jsonify({'error': 'Invalid flight'}), 400
    
    flight_data = flight_response.json()
    
    # Generate unique booking ID
    booking_id = f'BK{uuid.uuid4().hex[:6].upper()}'
    
    new_booking = Booking(
        booking_id=booking_id,
        user_id=data['user_id'],
        flight_code=data['flight_code'],
        flight_date=datetime.strptime(data['flight_date'], '%Y-%m-%d').date(),
        price=flight_data['price']
    )
    
    db.session.add(new_booking)
    db.session.commit()
    
    return jsonify(new_booking.to_dict()), 201

@app.route('/api/bookings/user/<int:user_id>', methods=['GET'])
def get_user_bookings(user_id):
    bookings = Booking.query.filter_by(user_id=user_id).all()
    return jsonify([booking.to_dict() for booking in bookings])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)