from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Room, Booking, Feedback, db
from datetime import datetime

bp = Blueprint('rooms', __name__)

@bp.route('/')
@jwt_required()
def list_rooms():
    building_filter = request.args.get('building')
    capacity_filter = request.args.get('capacity')
    
    query = Room.query
    if building_filter:
        query = query.filter(Room.building.ilike(f'%{building_filter}%'))
    if capacity_filter and capacity_filter.isdigit():
        query = query.filter(Room.capacity >= int(capacity_filter))
        
    rooms = query.all()
    buildings = db.session.query(Room.building).distinct().all()
    buildings = [b[0] for b in buildings]
    
    return render_template('rooms/list.html', rooms=rooms, buildings=buildings)

@bp.route('/<int:room_id>')
@jwt_required()
def view_room(room_id):
    room = Room.query.get_or_404(room_id)
    reviews = Feedback.query.filter_by(room_id=room_id).order_by(Feedback.created_at.desc()).all()
    return render_template('rooms/view.html', room=room, reviews=reviews)

@bp.route('/<int:room_id>/feedback', methods=['POST'])
@jwt_required()
def submit_feedback(room_id):
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    
    feedback = Feedback(
        user_id=int(get_jwt_identity()),
        room_id=room_id,
        rating=int(rating),
        comment=comment
    )
    db.session.add(feedback)
    db.session.commit()
    flash('Feedback submitted!', 'success')
    return redirect(url_for('rooms.view_room', room_id=room_id))
