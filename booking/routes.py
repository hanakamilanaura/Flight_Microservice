from flask import Blueprint, render_template

booking_bp = Blueprint('booking', __name__, template_folder='templates')

@booking_bp.route('/booking')
def booking_home():
    return render_template('booking.html')
