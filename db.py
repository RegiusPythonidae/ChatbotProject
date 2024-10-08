from models import User, Message, Course, UserCourse
from extensions import app, db

# One - To - One
# One - To - Many
# Many - To - Many

with app.app_context():
    db.create_all()