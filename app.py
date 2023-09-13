"""Blogly application."""
from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)

app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'bleepblapbloop'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route("/")
def base():
    """Change the user page to show the posts for that user."""
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("posts/homepage.html", posts=posts)

"""User route"""
"""Show all users. Make these links to view the detail page for the user. Have a link here to the add-user form."""
@app.route("/users")
def users_index():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("users/index.html", users=users)

"""Show an add form for users"""
@app.route("/users/new", methods=["GET"])
def users_new_form():
    return render_template("users/new.html")

"""Process the add form, adding a new user and going back to /users"""
@app.route("/users/new", methods = ["POST"])
def users_new():
    
    new_user = User (
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)
    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")

"""Show information about the given user. Have a button to get to their edit page, and to delete the user."""
@app.route("/users/<int:user_id>")
def users_show(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("users/show.html", user=user)

"""Show the edit page for a user. Have a cancel button that returns to the detail page for a user, and a save button that updates the user."""
@app.route("/users/<int:user_id>/edit")
def users_edit(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("users/edit.html", user=user)

"""Process the edit form, returning the user to the /users page."""
@app.route("/users/<int:user_id>/edit", methods=["POST"])
def users_update(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name=request.form["first_name"]
    user.last_name=request.form["last_name"]
    user.image_url=request.form["image_url"]

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

"""Delete the user."""
@app.route("/users/<int:user_id>/delete", methods=["POST"])
def users_delete(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

"""Post route"""
"""Show form to add a post for that user."""
@app.route("/users/<int:user_id>/posts/new")
def posts_new_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("posts/new.html", user=user)

"""Handle add form; add post and redirect to the user detail page."""
@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def posts_new(user_id):
    user = User.query.get_or_404(user_id)
    new_post = Post(
        title=request.form['title'],
        content=request.form['content'],
        user=user)
    db.session.add(new_post)
    db.session.commit()
    return redirect(f"/users/{user_id}")

"""Show a post. Show buttons to edit and delete the post."""
@app.route("/posts/<int:post_id>")
def show_posts(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("posts/show.html", post=post)

"""Show form to edit a post, and to cancel (back to user page)."""
@app.route("/posts/<int:post_id>/edit", methods=["GET"])
def posts_edit(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("posts/edit.html", post=post)

"""Handle editing of a post. Redirect back to the post view."""
@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def posts_update(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]

    db.session.add(post)
    db.session.commit()
    return redirect(f"/users/{post.user_id}")

"""Delete the post."""
@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_posts(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")