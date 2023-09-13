"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://freesvg.org/img/abstract-user-flat-4.png"

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)
    """Add foreign key to the User table"""
    posts = db.relationship("Post", backref='user', cascade="all, delete-orphan")
    """The @property decorator is used to create a property method called full_name for the User class. the @property decorator is used to define a method as a "getter" method for a class attribute."""
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")
    
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)