from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import StudyGroup, User, db

bp = Blueprint('groups', __name__)

@bp.route('/')
@jwt_required()
def list_groups():
    groups = StudyGroup.query.all()
    return render_template('groups/list.html', groups=groups)

@bp.route('/create', methods=['GET', 'POST'])
@jwt_required()
def create_group():
    if request.method == 'POST':
        name = request.form.get('name')
        module = request.form.get('module')
        description = request.form.get('description')
        
        group = StudyGroup(
            name=name,
            module=module,
            description=description,
            created_by_id=int(get_jwt_identity())
        )
        # Add creator as member
        current_user = User.query.get(int(get_jwt_identity()))
        group.members.append(current_user)
        
        db.session.add(group)
        db.session.commit()
        flash('Study Group created!', 'success')
        return redirect(url_for('groups.list_groups'))
        
    return render_template('groups/create.html')

@bp.route('/<int:group_id>/join', methods=['POST'])
@jwt_required()
def join_group(group_id):
    group = StudyGroup.query.get_or_404(group_id)
    current_user = User.query.get(int(get_jwt_identity()))
    
    if current_user not in group.members:
        group.members.append(current_user)
        db.session.commit()
        flash('Joined group successfully!', 'success')
    else:
        flash('You are already a member.', 'info')
        
    return redirect(url_for('groups.list_groups'))

@bp.route('/<int:group_id>/leave', methods=['POST'])
@jwt_required()
def leave_group(group_id):
    group = StudyGroup.query.get_or_404(group_id)
    current_user = User.query.get(int(get_jwt_identity()))
    
    if current_user in group.members:
        group.members.remove(current_user)
        db.session.commit()
        flash('You have left the group.', 'success')
    else:
        flash('You are not a member of this group.', 'error')
        
    return redirect(url_for('main.dashboard'))
