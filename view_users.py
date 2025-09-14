from extensions import db
from models import User
from app import create_app

app = create_app()
with app.app_context():
    users = User.query.all()
    print("ID | Username | Email")
    print("-------------------------")
    for u in users:
        print(f"{u.id} | {u.username} | {u.email}")
