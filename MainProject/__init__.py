from flask import Flask, render_template, redirect, url_for, request
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def App_Creation():
    app = Flask(__name__)
    app.config['Password'] = 'UserPassword'
    login_manager = LoginManager()
    login_manager.login_view = 'authorize'
    login_manager.init_app(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDB.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = '19980706'
    db.init_app(app)

    from .user_class import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    from .drink_class import Drink
    def index():
        drinks = Drink.query.all()  # 查询所有饮料
        return render_template('main.html', drinks=drinks)

    def drink(drink_id):
        return Drink.query.get(drink_id)

    from .blueprint import BP
    app.register_blueprint(BP)

    from .start import BPstart
    app.register_blueprint(BPstart)

    return app
