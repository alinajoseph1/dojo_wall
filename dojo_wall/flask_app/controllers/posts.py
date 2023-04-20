from flask_app import app
from flask import render_template, redirect, request, session, flash, get_flashed_messages
from flask_app.models.post import Post
from flask_app.models.user import User 

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/posts",methods=["POST"])
def create_post():
    print("in create route")
    print(request.form)
    Post.save(request.form)
    
    
    return redirect("/wall")

@app.route("/posts/delete/<post_id>")
def delete_post(post_id):
    print("Delete post - ", post_id)
    Post.delete(post_id)
    return redirect("/wall")

