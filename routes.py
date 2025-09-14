from flask import render_template, redirect, url_for, flash, session, request, abort
from extensions import db, bcrypt
from models import User, Task
from forms import RegisterForm, LoginForm, TaskForm

def register_routes(app):

    @app.route("/")
    def home():
        if "user_id" not in session:
            return redirect(url_for("login"))
        form = TaskForm()
        tasks = Task.query.filter_by(user_id=session["user_id"]).order_by(Task.id.desc()).all()
        return render_template("index.html", form=form, tasks=tasks)

    @app.route("/add_task", methods=["POST"])
    def add_task():
        if "user_id" not in session:
            return redirect(url_for("login"))
        form = TaskForm()
        if form.validate_on_submit():
            new_task = Task(title=form.title.data.strip(), status="Pending", user_id=session["user_id"])
            db.session.add(new_task)
            db.session.commit()
            flash("Task added successfully!", "success")
        else:
            flash("Couldn't add task. Check input.", "danger")
        return redirect(url_for("home"))

    @app.route("/update/<int:id>")
    def update_task(id):
        if "user_id" not in session:
            return redirect(url_for("login"))
        task = Task.query.get_or_404(id)
        if task.user_id != session["user_id"]:
            abort(403)
        task.status = "Working" if task.status=="Pending" else "Done" if task.status=="Working" else "Pending"
        db.session.commit()
        flash(f"Task status updated to {task.status}.", "info")
        return redirect(url_for("home"))

    @app.route("/delete/<int:id>")
    def delete_task(id):
        if "user_id" not in session:
            return redirect(url_for("login"))
        task = Task.query.get_or_404(id)
        if task.user_id != session["user_id"]:
            abort(403)
        db.session.delete(task)
        db.session.commit()
        flash("Task deleted!", "danger")
        return redirect(url_for("home"))

    @app.route("/clear")
    def clear_all():
        if "user_id" not in session:
            return redirect(url_for("login"))
        Task.query.filter_by(user_id=session["user_id"]).delete()
        db.session.commit()
        flash("All your tasks cleared.", "info")
        return redirect(url_for("home"))

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if "user_id" in session:
            return redirect(url_for("home"))
        form = RegisterForm()
        if form.validate_on_submit():
            existing = User.query.filter_by(email=form.email.data.strip().lower()).first()
            if existing:
                flash("Email already registered. Please login.", "warning")
                return redirect(url_for("login"))
            hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
            user = User(username=form.username.data.strip(), email=form.email.data.strip().lower(), password=hashed_pw)
            db.session.add(user)
            db.session.commit()
            flash("Account created! Please login.", "success")
            return redirect(url_for("login"))
        return render_template("register.html", form=form)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if "user_id" in session:
            return redirect(url_for("home"))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data.strip().lower()).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                session["user_id"] = user.id
                session["username"] = user.username
                flash("Login successful!", "success")
                return redirect(url_for("home"))
            flash("Invalid email or password.", "danger")
        return render_template("login.html", form=form)

    @app.route("/logout")
    def logout():
        session.pop("user_id", None)
        session.pop("username", None)
        flash("Logged out.", "info")
        return redirect(url_for("login"))
