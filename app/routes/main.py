from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Room, Booking, MaintenanceIssue

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/dashboard')
@jwt_required()
def dashboard():
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    
    context = {
        'user': user
    }
    
    if user.role == 'Admin':
        context['total_users'] = User.query.count()
        context['total_rooms'] = Room.query.count()
        context['active_issues'] = MaintenanceIssue.query.filter(MaintenanceIssue.status != 'Resolved').count()
    elif user.role == 'Student' or user.role == 'Staff':
        context['my_bookings'] = Booking.query.filter_by(user_id=user.id).all()
        
    return render_template('dashboard.html', **context)
