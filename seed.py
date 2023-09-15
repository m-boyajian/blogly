"""Seed file to make sample data for db."""
from models import User, Post, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

User.query.delete()
Post.query.delete()

"""Fake user content"""
alan= User(first_name="Alan", last_name="Alda", image_url="https://freesvg.org/img/abstract-user-flat-4.png")
joel= User(first_name="Joel", last_name="Burton", image_url="https://freesvg.org/img/abstract-user-flat-4.png")
jane= User(first_name="Jane", last_name="Smith", image_url="https://freesvg.org/img/abstract-user-flat-4.png")

db.session.add_all([alan, joel, jane])
db.session.commit()