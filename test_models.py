from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///test_models_db"
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

