from app.extensions import db
from datetime import datetime

# Association table for Group Membership
group_membership = db.Table('group_membership',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('study_group.id'), primary_key=True),
    db.Column('joined_at', db.DateTime, default=datetime.utcnow)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='Student') # Student, Staff, Admin, Facilities
    
    bookings = db.relationship('Booking', backref='user', lazy=True)
    feedback = db.relationship('Feedback', backref='user', lazy=True)
    reported_issues = db.relationship('MaintenanceIssue', foreign_keys='MaintenanceIssue.reported_by_id', backref='reporter', lazy=True)
    assigned_issues = db.relationship('MaintenanceIssue', foreign_keys='MaintenanceIssue.assigned_to_id', backref='assignee', lazy=True)
    created_groups = db.relationship('StudyGroup', backref='creator', lazy=True)
    groups = db.relationship('StudyGroup', secondary=group_membership, back_populates='members')

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    building = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    equipment = db.Column(db.String(200)) # Comma separated list
    room_type = db.Column(db.String(50)) # Study, Lab, Lecture Hall
    status = db.Column(db.String(20), default='Available') # Available, Maintenance
    
    bookings = db.relationship('Booking', backref='room', lazy=True)
    issues = db.relationship('MaintenanceIssue', backref='room', lazy=True)
    feedback = db.relationship('Feedback', backref='room', lazy=True)
    usage_data = db.relationship('UsageData', backref='room', uselist=False, lazy=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='Confirmed') # Confirmed, Cancelled, Completed

class MaintenanceIssue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    reported_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    description = db.Column(db.Text, nullable=False)
    issue_type = db.Column(db.String(50)) # Equipment, Cleanliness, etc.
    priority = db.Column(db.String(20), default='Medium') # Low, Medium, High
    status = db.Column(db.String(20), default='Open') # Open, In Progress, Resolved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime, nullable=True)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False) # 1-5
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class StudyGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    module = db.Column(db.String(50))
    description = db.Column(db.Text)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    members = db.relationship('User', secondary=group_membership, back_populates='groups')

class UsageData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), unique=True, nullable=False)
    total_bookings = db.Column(db.Integer, default=0)
    current_occupancy = db.Column(db.Integer, default=0)
    utilization_rate = db.Column(db.Float, default=0.0)
