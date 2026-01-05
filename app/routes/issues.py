from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import MaintenanceIssue, Room, User, db

bp = Blueprint('issues', __name__)

@bp.route('/')
@jwt_required()
def list_issues():
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    
    if user.role in ['Admin', 'Facilities']:
        issues = MaintenanceIssue.query.all()
    else:
        issues = MaintenanceIssue.query.filter_by(reported_by_id=current_user_id).all()
        
    return render_template('maintenance/list.html', issues=issues, user=user)

@bp.route('/report', methods=['GET', 'POST'])
@jwt_required()
def report_issue():
    if request.method == 'POST':
        room_id = request.form.get('room_id')
        description = request.form.get('description')
        priority = request.form.get('priority')
        issue_type = request.form.get('issue_type')
        
        issue = MaintenanceIssue(
            room_id=int(room_id),
            reported_by_id=int(get_jwt_identity()),
            description=description,
            priority=priority,
            issue_type=issue_type
        )
        db.session.add(issue)
        db.session.commit()
        flash('Issue reported successfully.', 'success')
        return redirect(url_for('issues.list_issues'))
        
    rooms = Room.query.all()
    return render_template('maintenance/report.html', rooms=rooms)

@bp.route('/<int:issue_id>/update', methods=['POST'])
@jwt_required()
def update_status(issue_id):
    current_user_id = int(get_jwt_identity())
    user = User.query.get(current_user_id)
    
    if user.role not in ['Admin', 'Facilities']:
        flash('Unauthorized', 'error')
        return redirect(url_for('issues.list_issues'))
        
    issue = MaintenanceIssue.query.get_or_404(issue_id)
    status = request.form.get('status')
    if status:
        issue.status = status
        db.session.commit()
        
    return redirect(url_for('issues.list_issues'))
