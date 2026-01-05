# SmartCampus Management System

## Project Overview
A comprehensive web application for managing university campus resources. This system integrates room booking, maintenance reporting, and study group coordination into a unified platform.

## Features
- **Role-Based Access Control**: Tailored dashboards for Students, Staff, Facilities, and Admins.
- **Room Booking**: Real-time availability checks with conflict detection.
- **Maintenance Tracking**: Report and track facility issues from "Open" to "Resolved".
- **Study Groups**: Create and join academic study groups.
- **Reviews**: Rate and review rooms.

## Tech Stack
- **Backend**: Python, Flask, SQLAlchemy, Marshmallow
- **Database**: MySQL (compatible with SQLite for dev)
- **Frontend**: HTML5, TailwindCSS (Jinja2 Templates)
- **Authentication**: JWT (JSON Web Tokens)

## Project Structure
```
smartcampus/
├── app.py              # Entry point
├── config.py           # Configuration
├── models.py           # Database Models (in app/)
├── schemas.py          # Marshmallow Schemas
├── app/
│   ├── routes/         # Application logic
│   │   ├── auth.py
│   │   ├── rooms.py
│   │   ├── bookings.py
│   │   ├── issues.py
│   │   ├── groups.py
│   ├── templates/      # HTML Templates
│   ├── static/         # Static assets
├── requirements.txt
└── README.md
```

## Setup Instructions

1. **Install Dependencies**
   ```bash
   python -m pip install -r requirements.txt
   ```

2. **Configure Database**
   - Create a `.env` file in the root directory.
   - Add your database URL:
     ```
     DATABASE_URL=mysql+pymysql://user:password@localhost/smartcampus
     ```
   - If no `.env` is provided, it defaults to SQLite (`smartcampus.db`).

3. **Run the Application**
   ```bash
   python app.py
   ```
   Access at `http://127.0.0.1:5000`

## Test Accounts
- **Student**: student@university.ac.uk / student123
- **Admin**: admin@university.ac.uk / admin123
- **Facilities**: facilities@university.ac.uk / facilities123
