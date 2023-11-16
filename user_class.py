from flask_login import UserMixin
from . import db


# 以下数据需从数据库抓取

class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), unique=True, nullable=False)
    user_email = db.Column(db.String(120), unique=True, nullable=False)
    user_password = db.Column(db.String(120), nullable=False)
    user_weight = db.Column(db.Integer)
    user_height = db.Column(db.Integer)
    user_age = db.Column(db.Integer)
# new_user = User(user_name='john', user_email='john@example.com', user_password='password123')
# db.session.add(new_user)
# db.session.commit()
# user = User.query.filter_by(username='john').first()
# user.email = 'new_email@example.com'
# db.session.commit()

# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField
# from wtforms.validators import DataRequired, Length, EqualTo


# class RegistrationForm(FlaskForm):
#    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
#    email = StringField('Email', validators=[DataRequired(), Length(min=6, max=50)])
#    password = PasswordField('Password', validators=[DataRequired()])
#    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
#    submit = SubmitField('Sign Up')
