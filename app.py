from flask import Flask, render_template

# Import blueprints
from booking.routes import booking_bp
from flight.routes import flight_bp
from user.routes import user_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(booking_bp)
app.register_blueprint(flight_bp)
app.register_blueprint(user_bp)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)