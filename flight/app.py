from flask import Flask, jsonify, request, render_template
from models import db, Flight
from datetime import datetime

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost:5432/flight_service_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/flight')
def flight_service():
    flights = Flight.query.all()
    return render_template('flight.html', flights=flights)

@app.route('/api/flights', methods=['GET'])
def get_flights():
    flights = Flight.query.all()
    return jsonify([flight.to_dict() for flight in flights])

@app.route('/api/flights/<flight_code>', methods=['GET'])
def get_flight(flight_code):
    flight = Flight.query.filter_by(flight_code=flight_code).first_or_404()
    return jsonify(flight.to_dict())

@app.route('/api/flights', methods=['POST'])
def create_flight():
    data = request.json
    
    new_flight = Flight(
        flight_code=data['flight_code'],
        airline_name=data['airline_name'],
        departure_time=datetime.strptime(data['departure_time'], '%H:%M:%S').time(),
        departure_city=data['from'],
        arrival_city=data['to'],
        price=data['price']
    )
    
    db.session.add(new_flight)
    db.session.commit()
    
    return jsonify(new_flight.to_dict()), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)