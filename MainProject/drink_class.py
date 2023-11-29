from . import db


class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    drink_name = db.Column(db.String(120), unique=True, nullable=False)
    drink_water = db.Column(db.Float, nullable=False)
    drink_energy = db.Column(db.Float, nullable=False)
    drink_protein = db.Column(db.Float,  nullable=False)
    drink_sugar = db.Column(db.Float,  nullable=False)
    drink_caffeine = db.Column(db.Float, nullable=False)