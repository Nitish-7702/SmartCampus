from app import create_app, db
from app.models import User, Room

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Room': Room}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("DATABASE ENGINE:", db.engine.url)

    app.run(debug=True, port=5000)
