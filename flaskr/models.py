from flaskr import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id: int = db.Column(db.Integer, primary_key = True)
    email: str = db.Column(db.String(20), nullable=False, unique=True)
    password: str = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"User('{self.email}')"
