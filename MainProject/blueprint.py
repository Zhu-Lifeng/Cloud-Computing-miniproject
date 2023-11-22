from flask import Blueprint, render_template, request, url_for, flash, redirect
from .user_class import User
from .drink_class import Drink
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
    # print(USER_email,USER_password)
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
                    user_password=generate_password_hash(USER_password, method='pbkdf2:sha256'),
                    user_weight=80, user_height=180, user_age=25)

    # 这里把新用户数据传到数据库里
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

    # 这里要把用户数据更新到数据库里

    return redirect(url_for('my_blueprint.main'))


@BP.route('/main')
@login_required
def main():
    return render_template('main.html', user=current_user, drinks=Drink.query.with_entities(Drink.drink_name).all())


@BP.route('/view')
@login_required
def view():
    return render_template('view.html', user=current_user)  # , name=current_user.user_name)


@BP.route('/drink_add', methods=['POST'])
@login_required
def drink_add():
    DRINK_name = request.form.get('drink_name')
    DRINK_water = request.form.get('drink_water')
    DRINK_energy = request.form.get('drink_energy')
    DRINK_protein = request.form.get('drink_protein')
    DRINK_sugar = request.form.get('drink_sugar')
    DRINK_caffeine = request.form.get('drink_caffeine')

    DRINK = Drink.query.filter_by(drink_name=DRINK_name).first()

    if DRINK:
        flash('This drink already exists')
        return redirect(url_for('my_blueprint.main'))

    NEW_DRINK = Drink(drink_name=DRINK_name, drink_water=DRINK_water, drink_energy=DRINK_energy,
                      drink_protein=DRINK_protein, drink_sugar=DRINK_sugar, drink_caffeine=DRINK_caffeine)
    db.session.add(NEW_DRINK)
    db.session.commit()

    return redirect(url_for('my_blueprint.main'))


@BP.route('/result', methods=['POST'])
@login_required
def result():
    # 获取用户选择的数据类型
    select_water = 'select_water' in request.form
    select_energy = 'select_energy' in request.form
    select_protein = 'select_protein' in request.form
    select_sugar = 'select_sugar' in request.form
    select_caffeine = 'select_caffeine' in request.form

    # 初始化计算结果
    total_water = 0
    total_energy = 0
    total_protein = 0
    total_sugar = 0
    total_caffeine = 0

    for drink in Drink.query.all():
        drink_number_key = f'drink_number_{drink.drink_name}'
        drink_number = request.form.get(drink_number_key)
        if drink_number:
            drink_number = int(drink_number)
            if select_water:
                total_water += drink.drink_water * drink_number
            if select_energy:
                total_energy += drink.drink_energy * drink_number
            if select_protein:
                total_protein += drink.drink_protein * drink_number
            if select_sugar:
                total_sugar += drink.drink_sugar * drink_number
            if select_caffeine:
                total_caffeine += drink.drink_caffeine * drink_number

    # 将计算结果传递给模板
    return render_template('result.html', 
                           select_water=select_water, total_water=total_water,
                           select_energy=select_energy, total_energy=total_energy,
                           select_protein=select_protein, total_protein=total_protein,
                           select_sugar=select_sugar, total_sugar=total_sugar,
                           select_caffeine=select_caffeine, total_caffeine=total_caffeine)



@BP.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('start.index'))
