from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import validates

db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    _password_hash = db.Column(db.String(128), nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.String(500), nullable=True)

    # Relationships
    recipes = db.relationship(
        'Recipe',
        backref='user',
        lazy=True,
        cascade='all, delete-orphan')

    # Validations
    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise ValueError("Username is required")
        if User.query.filter(User.username == username).first():
            raise ValueError("Username must be unique")
        return username

    @validates('image_url')
    def validate_image_url(self, key, image_url):
        if not image_url:
            raise ValueError("Image URL is required")
        return image_url

    @validates('bio')
    def validate_bio(self, key, bio):
        if not bio:
            raise ValueError("Bio is required")
        return bio

    # Password handling with bcrypt
    @property
    def password_hash(self):
        raise AttributeError('Password hashes may not be viewed.')

    @password_hash.setter
    def password_hash(self, password):
        if password and len(password) >= 6:
            self._password_hash = bcrypt.generate_password_hash(
                password).decode('utf-8')
        else:
            raise ValueError("Password must be at least 6 characters long")

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'image_url': self.image_url,
            'bio': self.bio
        }

    def __repr__(self):
        return f'<User {self.username}>'


class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    instructions = db.Column(db.String(1000), nullable=False)
    minutes_to_complete = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Database constraint for instructions length
    __table_args__ = (
        CheckConstraint(
            'length(instructions) >= 50',
            name='instructions_min_length'),
    )

    # Validations
    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Title is required")
        return title

    @validates('instructions')
    def validate_instructions(self, key, instructions):
        if not instructions:
            raise ValueError("Instructions are required")
        if len(instructions) < 50:
            raise ValueError(
                "Instructions must be at least 50 characters long")
        return instructions

    @validates('minutes_to_complete')
    def validate_minutes(self, key, minutes):
        if not isinstance(minutes, int) or minutes <= 0:
            raise ValueError("Minutes to complete must be a positive integer")
        return minutes

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'instructions': self.instructions,
            'minutes_to_complete': self.minutes_to_complete,
            'user': self.user.to_dict()
        }

    def __repr__(self):
        return f'<Recipe {self.title}>'
