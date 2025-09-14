from extensions import db
from models import User
from app import create_app

app = create_app()
with app.app_context():
    user = User.query.filter_by(email='dar@gmail.com').first()
    if user:
        db.session.delete(user)
        db.session.commit()
        print("User deleted!")
    else:
        print("User not found")
