from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Flight(db.Model):
    __tablename__ = 'flights'
    
    id = db.Column(db.Integer, primary_key=True)
    flight_code = db.Column(db.String(10), unique=True, nullable=False)
    airline_name = db.Column(db.String(100), nullable=False)
    departure_time = db.Column(db.Time, nullable=False)
    departure_city = db.Column(db.String(100), nullable=False)
    arrival_city = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(20), default='On Time')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'flight_code': self.flight_code,
            'airline_name': self.airline_name,
            'departure_time': self.departure_time.strftime('%H:%M:%S'),
            'from': self.departure_city,
            'to': self.arrival_city,
            'price': float(self.price),
            'status': self.status
        }
