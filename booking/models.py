from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.String(10), unique=True, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    flight_code = db.Column(db.String(10), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    flight_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='Pending')
    price = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'booking_id': self.booking_id,
            'user_id': self.user_id,
            'flight_code': self.flight_code,
            'booking_date': self.booking_date.isoformat(),
            'flight_date': self.flight_date.isoformat(),
            'status': self.status,
            'price': float(self.price)
        }
