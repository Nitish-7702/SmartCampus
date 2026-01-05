from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Booking, Room, db
from datetime import datetime

bp = Blueprint('bookings', __name__)

@bp.route('/book/<int:room_id>', methods=['POST'])
@jwt_required()
def book_room(room_id):
    user_id = int(get_jwt_identity())
    
    # Handle both Form data (Frontend) and JSON (API clients)
    if request.is_json:
        data = request.get_json()
        start_time_str = data.get('start_time')
        end_time_str = data.get('end_time')
    else:
        start_time_str = request.form.get('start_time')
        end_time_str = request.form.get('end_time')
    
    try:
        start_time = datetime.fromisoformat(start_time_str)
        end_time = datetime.fromisoformat(end_time_str)
        
        if start_time >= end_time:
             if request.is_json:
                 return jsonify({"error": "End time must be after start time"}), 400
             flash('End time must be after start time.', 'error')
             return redirect(url_for('rooms.view_room', room_id=room_id))

        # Conflict detection
        conflict = Booking.query.filter(
            Booking.room_id == room_id,
            Booking.status == 'Confirmed',
            Booking.start_time < end_time,
            Booking.end_time > start_time
        ).first()
        
        if conflict:
            if request.is_json:
                return jsonify({"error": "Room is already booked for this time slot"}), 409
            flash('Room is already booked for this time slot.', 'error')
            return redirect(url_for('rooms.view_room', room_id=room_id))
            
        booking = Booking(
            user_id=user_id,
            room_id=room_id,
            start_time=start_time,
            end_time=end_time
        )
        db.session.add(booking)
        db.session.commit()
        
        if request.is_json:
            return jsonify({"message": "Booking confirmed", "booking_id": booking.id}), 201
            
        flash('Booking confirmed!', 'success')
        return redirect(url_for('main.dashboard'))
        
    except ValueError:
        if request.is_json:
            return jsonify({"error": "Invalid date format"}), 400
        flash('Invalid date format.', 'error')
        return redirect(url_for('rooms.view_room', room_id=room_id))

@bp.route('/<int:booking_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    current_user_id = int(get_jwt_identity())
    
    if booking.user_id != current_user_id:
        flash('Unauthorized to cancel this booking.', 'error')
        return redirect(url_for('main.dashboard'))
        
    booking.status = 'Cancelled'
    db.session.commit()
    flash('Booking cancelled successfully.', 'success')
    return redirect(url_for('main.dashboard'))
