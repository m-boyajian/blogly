from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///test_models_db"
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    """Tests for model for Users."""
    def setUp(self):
        User.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()
    
    def test_user_index(self):
        
