from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

# Define your models here
class Flavor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    seasonal = db.Column(db.String(50), nullable=True)

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ingredient = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class Suggestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flavor_id = db.Column(db.Integer, db.ForeignKey('flavor.id'), nullable=False)
    allergies = db.Column(db.String(250), nullable=True)
    flavor = db.relationship('Flavor', backref=db.backref('suggestions', lazy=True))
