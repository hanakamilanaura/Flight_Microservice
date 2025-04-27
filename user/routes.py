from flask import Blueprint, render_template

user_bp = Blueprint('user', __name__, template_folder='templates')

@user_bp.route('/user')
def user_home():
        return render_template('user.html')