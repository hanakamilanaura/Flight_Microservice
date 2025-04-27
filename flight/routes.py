from flask import Blueprint, render_template

flight_bp = Blueprint('flight', __name__, template_folder='templates')

@flight_bp.route('/flight')
def flight_home():
    return render_template('flight.html')