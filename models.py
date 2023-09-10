"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://freesvg.org/img/abstract-user-flat-4.png"

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)

    """The @property decorator is used to create a property method called full_name for the User class. the @property decorator is used to define a method as a "getter" method for a class attribute."""
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)