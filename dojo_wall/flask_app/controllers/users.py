from flask_app import app
from flask import render_template, redirect, request, session, flash, get_flashed_messages
from flask_app.models.user import User
from flask_app.models.post import Post
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("create.html")

@app.route("/new-user", methods=["POST"])
def new_user():
    if not User.validate_register(request.form):
        return redirect("/")
    
    data = {
        "fname": request.form["fname"],
        "lname": request.form["lname"],
        "email": request.form["email"],
        "username": request.form["username"],
        "password": bcrypt.generate_password_hash(request.form["password"])

    }
    id = User.save(data)
    session["user_id"] = id 
    
    return redirect("/login")

@app.route('/login', methods=['GET'])
def login_form():
    return render_template("login.html")


@app.route('/login', methods=['POST'])
def login_authenticate():
    data = {
        "email": request.form["email"]
    }
    user = User.get_email(data)
    if not user:
        flash("Invalid email or password")
        return redirect("/login")
    
    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        flash("Invalid password")
        return redirect("/login")
    
    session["user_id"] = user.id

    return redirect("/wall")



@app.route('/wall', methods=["GET"])
def wall():
    
    if "user_id" not in session:
        flash("You need to login first! :) ")
        return redirect("/login")
    
    data = {
        "id" : session["user_id"]
    }
    user = User.get_one(data)
    all_posts = Post.get_all()
    
    return render_template("wall.html", user=user, posts=all_posts)

@app.route('/logout')
def logout_user():
    session.clear()
    return redirect("/")
