from flask import Blueprint, render_template, request, url_for,flash, redirect
from .user_class import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user,login_required
BP = Blueprint('my_blueprint', __name__)


@BP.route('/login')
def login():
    return render_template('login.html')

@BP.route('/login',methods=['POST'])
def login_post():
    USER_email = request.form.get('user_email')
    USER_password = request.form.get('user_password')
    USER= User.query.filter_by(user_email=USER_email).first()#本处query需按最终使用db类型修正函数

    if not USER or not check_password_hash(USER.password,USER_password):
        flash ('Please check your e-mail address or password.')
        return redirect (url_for('BP.login'))

    login_user(USER)
    return redirect(url_for('main.html'))


@BP.route('/signup')
def signup():
    return render_template('signin.html')


@BP.route('/signup',method=['POST'])
def signup_post():
    USER_email = request.form.get('user_email')
    USER_password = request.form.get('user_password')
    USER_name=request.form.get('user_name')

    USER=User.query.filter_by(user_email=USER_email).first()

    if USER:
        flash('Email address already exists')
        return redirect(url_for('BP.signup'))

    NEW_USER = User(user_email = USER_email, user_name = USER_name, user_password = generate_password_hash(USER_password, method='sha256'))

    ##这里要把新用户数据传到数据库里

    return redirect(url_for('BP.filling'))
@BP.route('/filling')
def filling():
    return render_template('filling.html')
@BP.route('/filling',method=['PUT'])
def filling_put():
    USER_weight = request.form.get('user_weight')
    USER_height = request.form.get('user_height')
    USER_age = request.form.get('user_age')
    USER_name = request.form.get('user_name')

    USER=User(user_weight=USER_weight, user_height = USER_height, user_age = USER_age, user_name= USER_name)

    ##这里要把用户数据更新到数据库里
    return redirect(url_for('BP.main'))

@BP.route('/main')
def main():
    return render_template('main.html')

@BP.route('/main',method=['GET'])
def main_buttons():
    if 'view' in request.form:
        return redirect(url_for('BP.view'))
    elif 'calculate' in request.form:
        return render_template('result.html')

@BP.route('/view')
def view():
    return render_template('view.html')

@BP.route('/view',method=['POST'])
def view_post():
    return redirect(url_for('BP.filling'))


def result():
    return render_template('result.html')
