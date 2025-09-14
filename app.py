from flask import Flask
from extensions import db, bcrypt, csrf

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config["SECRET_KEY"] = "supersecretkey"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # init extensions
    db.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)

    # import models before creating tables
    with app.app_context():
        from models import User, Task
        db.create_all()

    # register routes
    from routes import register_routes
    register_routes(app)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
