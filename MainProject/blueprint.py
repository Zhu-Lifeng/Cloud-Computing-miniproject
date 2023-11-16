from flask import Blueprint, render_template, request, url_for, flash, redirect
from .user_class import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from . import db
BP = Blueprint('my_blueprint', __name__)


@BP.route('/login')
def login():
    return render_template('login.html')


@BP.route('/login', methods=['POST'])
def login_post():
    USER_email = request.form['user_email']
    USER_password = request.form['user_password']
    #print(USER_email,USER_password)
    USER = User.query.filter_by(user_email=USER_email).first()  # 本处query需按最终使用db类型修正函数

    if not USER or not check_password_hash(USER.user_password, USER_password):
        flash('Please check your e-mail address or password.')
        return redirect(url_for('my_blueprint.login'))

    login_user(USER)
    return redirect(url_for('my_blueprint.main'))


@BP.route('/signup')
def signup():
    return render_template('signup.html')


@BP.route('/signup', methods=['POST'])
def signup_post():
    USER_email = request.form.get('user_email')
    USER_password = request.form.get('user_password')
    USER_name = request.form.get('user_name')

    USER = User.query.filter_by(user_email=USER_email).first()

    if USER:
        flash('Email address already exists')
        return redirect(url_for('my_blueprint.signup'))

    NEW_USER = User(user_email=USER_email, user_name=USER_name,
                    user_password=generate_password_hash(USER_password, method='sha256'),
                    user_weight=80,user_height=180,user_age=25)

    ##这里要把新用户数据传到数据库里
    db.session.add(NEW_USER)
    db.session.commit()

    login_user(NEW_USER)
    return redirect(url_for('my_blueprint.filling'))


@BP.route('/filling')
@login_required
def filling():
    return render_template('filling.html', user=current_user)


@BP.route('/filling', methods=['POST'])
@login_required
def filling_post():
    # 这地方按说应该用PUT,但是HTML写的网页只支持POST和GET，要用PUT需要使用JavaScript,待探究
    current_user.user_weight = request.form.get('user_weight')
    current_user.user_height = request.form.get('user_height')
    current_user.user_age = request.form.get('user_age')

    db.session.commit()

    ##这里要把用户数据更新到数据库里
    return redirect(url_for('my_blueprint.main'))


@BP.route('/main')
@login_required
def main():

    return render_template('main.html', user=current_user)


@BP.route('/view')
@login_required
def view():
    return render_template('view.html',user=current_user)  # , name=current_user.user_name)


#@BP.route('/view', methods=['GET'])
#@login_required
#def view_get():
#    return render_template('view.html', name=current_user.user_name)
# 此处需要与数据库联通，暂不清楚是这里拿数据还是在HTML里拿数据————————————————————————

@BP.route('/result')
@login_required
# 此处需要与数据库联通，暂不清楚是这里拿数据还是在HTML里拿数据
def result():
    return render_template('result.html')


@BP.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('start.index'))
