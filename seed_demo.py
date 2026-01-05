from app import create_app, db
from app.models import User, Room, StudyGroup, MaintenanceIssue, Booking, Feedback
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

app = create_app()

def seed_demo():
    with app.app_context():
        print("Checking and populating demo data...")
        
        # 1. Users
        users = {
            "Student": User.query.filter_by(email="student@university.ac.uk").first(),
            "Admin": User.query.filter_by(email="admin@university.ac.uk").first(),
            "Facilities": User.query.filter_by(email="facilities@university.ac.uk").first(),
            "Staff": User.query.filter_by(email="staff@university.ac.uk").first()
        }

        if not users["Student"]:
            print("Creating Student...")
            users["Student"] = User(full_name="John Student", email="student@university.ac.uk", password_hash=generate_password_hash("student123"), role="Student")
            db.session.add(users["Student"])
        
        if not users["Admin"]:
            print("Creating Admin...")
            users["Admin"] = User(full_name="Admin User", email="admin@university.ac.uk", password_hash=generate_password_hash("admin123"), role="Admin")
            db.session.add(users["Admin"])
            
        if not users["Facilities"]:
            print("Creating Facilities User...")
            users["Facilities"] = User(full_name="Jane Facilities", email="facilities@university.ac.uk", password_hash=generate_password_hash("facilities123"), role="Facilities")
            db.session.add(users["Facilities"])

        if not users["Staff"]:
            print("Creating Academic Staff...")
            users["Staff"] = User(full_name="Dr. Alan Turing", email="staff@university.ac.uk", password_hash=generate_password_hash("staff123"), role="Staff")
            db.session.add(users["Staff"])

        db.session.commit()

        # 2. Rooms
        if Room.query.count() == 0:
            print("Creating Rooms...")
            rooms = [
                Room(name="Library Study 1", building="Library", capacity=4, equipment="Whiteboard, Power Outlets", room_type="Study Room"),
                Room(name="Library Study 2", building="Library", capacity=6, equipment="TV Screen, Whiteboard", room_type="Study Room"),
                Room(name="Computer Lab A", building="Science Block", capacity=30, equipment="30 High-spec PCs, Projector", room_type="Lab"),
                Room(name="Lecture Hall 1", building="Main Building", capacity=150, equipment="Projector, Microphone, Stage", room_type="Lecture Hall"),
                Room(name="Project Room B", building="Innovation Centre", capacity=8, equipment="Smartboard, Conference Phone", room_type="Meeting Room"),
            ]
            db.session.add_all(rooms)
            db.session.commit()
        else:
            print("Rooms already exist.")

        # 3. Study Groups
        if StudyGroup.query.count() == 0:
            print("Creating Study Groups...")
            groups = [
                StudyGroup(name="Web Dev Projects", module="CMP5387", description="Working on Flask and React projects. Beginners welcome!", created_by_id=users["Student"].id),
                StudyGroup(name="Data Science Club", module="CMP6000", description="Discussing machine learning and python.", created_by_id=users["Student"].id),
                StudyGroup(name="Exam Prep: Algorithms", module="CMP4000", description="Grinding Leetcode and past papers.", created_by_id=users["Student"].id),
            ]
            # Add student to groups
            for g in groups:
                g.members.append(users["Student"])
            
            db.session.add_all(groups)
            db.session.commit()
        else:
            print("Study Groups already exist.")

        # 4. Maintenance Issues
        if MaintenanceIssue.query.count() == 0:
            print("Creating Maintenance Issues...")
            room_lab = Room.query.filter_by(name="Computer Lab A").first()
            room_hall = Room.query.filter_by(name="Lecture Hall 1").first()
            
            issues = [
                MaintenanceIssue(room_id=room_lab.id, reported_by_id=users["Staff"].id, description="PC #12 not turning on", priority="Medium", status="Resolved", issue_type="Equipment"),
                MaintenanceIssue(room_id=room_hall.id, reported_by_id=users["Student"].id, description="Projector flickering during lectures", priority="High", status="Open", issue_type="Electrical"),
            ]
            db.session.add_all(issues)
            db.session.commit()
        else:
            print("Maintenance Issues already exist.")
            
        # 5. Bookings
        if Booking.query.count() == 0:
            print("Creating Sample Bookings...")
            room_study = Room.query.filter_by(name="Library Study 1").first()
            
            # Booking for tomorrow 10am-12pm
            tomorrow = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0) + timedelta(days=1)
            booking = Booking(
                user_id=users["Student"].id,
                room_id=room_study.id,
                start_time=tomorrow,
                end_time=tomorrow + timedelta(hours=2),
                status="Confirmed"
            )
            db.session.add(booking)
            db.session.commit()
        else:
            print("Bookings already exist.")

        # 6. Reviews
        if Feedback.query.count() == 0:
            print("Creating Reviews...")
            room_study = Room.query.filter_by(name="Library Study 1").first()
            feedback = Feedback(
                user_id=users["Student"].id,
                room_id=room_study.id,
                rating=5,
                comment="Great room, very quiet and good wifi."
            )
            db.session.add(feedback)
            db.session.commit()

        print("Demo data seeding complete!")

if __name__ == "__main__":
    seed_demo()
