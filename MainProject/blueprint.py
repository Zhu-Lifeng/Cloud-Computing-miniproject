from flask import Blueprint, render_template, request, url_for, flash, redirect
from .user_class import User
from .drink_class import Drink
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from . import db
import requests
from PIL import Image
import os
BP = Blueprint('my_blueprint', __name__)


def picture():
    image_default = Image.open("MainProject/static/maxresdefault.jpg")
    response = requests.get("https://coffee.alexflipnote.dev/random.json")
    if response.status_code == 200:
        data = response.json()
        image_data = requests.get(data.get('file')).content
        image_path = os.path.join('MainProject/static/', 'background.jpg')
        with open(image_path, 'wb') as f:
            f.write(image_data)
        return image_path
    else:
        image_path = os.path.join('MainProject/static/', 'background.jpg')
        image_default.save(image_path, 'background.jpg')
        return image_path



@BP.route('/login')
def login():
    picture()
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
    picture()
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
                    user_weight=80, user_height=180, user_age=25, user_gender ='X')

    # 这里把新用户数据传到数据库里
    db.session.add(NEW_USER)
    db.session.commit()

    login_user(NEW_USER)
    return redirect(url_for('my_blueprint.filling'))


@BP.route('/filling')
@login_required
def filling():
    picture()
    return render_template('filling.html', user=current_user)


@BP.route('/filling', methods=['POST'])
@login_required
def filling_post():
    # 这地方按说应该用PUT,但是HTML写的网页只支持POST和GET，要用PUT需要使用JavaScript,待探究
    current_user.user_weight = request.form.get('user_weight')
    current_user.user_height = request.form.get('user_height')
    current_user.user_age = request.form.get('user_age')
    current_user.user_gender = request.form.get('user_gender')
    db.session.commit()

    # 这里要把用户数据更新到数据库里

    return redirect(url_for('my_blueprint.main'))


@BP.route('/main')
@login_required
def main():
    picture()
    return render_template('main.html', user=current_user, drinks=Drink.query.with_entities(Drink.drink_name).all())


@BP.route('/view')
@login_required
def view():
    picture()
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

    for drink in Drink.query.with_entities(Drink.drink_name).all():
        drink_number_key = f'drink_number_{drink.drink_name}'
        drink_number = request.form.get(drink_number_key)
        if drink_number:
            drink_number = int(drink_number)
            if select_water:
                DRINK_water = Drink.query.with_entities(Drink.drink_water).filter_by(drink_name=drink.drink_name).first()
                total_water += DRINK_water.drink_water * drink_number/100
            if select_energy:
                DRINK_energy = Drink.query.with_entities(Drink.drink_energy).filter_by(drink_name=drink.drink_name).first()
                total_energy += DRINK_energy.drink_energy * drink_number/100
            if select_protein:
                DRINK_protein = Drink.query.with_entities(Drink.drink_protein).filter_by(drink_name=drink.drink_name).first()
                total_protein += DRINK_protein.drink_protein * drink_number/100
            if select_sugar:
                DRINK_sugar = Drink.query.with_entities(Drink.drink_sugar).filter_by(drink_name=drink.drink_name).first()
                total_sugar += DRINK_sugar.drink_sugar * drink_number/100
            if select_caffeine:
                DRINK_caffeine = Drink.query.with_entities(Drink.drink_caffeine).filter_by(drink_name=drink.drink_name).first()
                total_caffeine += DRINK_caffeine.drink_caffeine * drink_number/100


    water_suggestion = ''
    energy_suggestion = ''
    protein_suggestion = ''
    sugar_suggestion = ''
    caffeine_suggestion = ''
    if current_user.user_gender == "male":
        F=5
    else:
        F=-161

    if select_water:
        recommand_water = current_user.user_weight*35
        if recommand_water > total_water :
            water_suggestion = 'You need intake more water! Your water intake today is ' + str(recommand_water - total_water)+'g less than the recommandation.'
        else:
            water_suggestion = 'Congratulation! Your water intake is enough for the day!'
    if select_energy:
        recommand_energy = current_user.user_weight*10+current_user.user_height*6.25-current_user.user_age*5+F
        if recommand_energy/2 < total_energy:
            energy_suggestion = ('The energy you intake from the beverages has exceeded half of your daily need! '
                                 'Please control your beverages intake.')
        else:
            energy_suggestion = f'You get {(total_energy/recommand_energy*100):.1f} % of your daily energy from beverages.'
    if select_protein:
        recommand_protein = current_user.user_weight*1.5
        protein_suggestion = f'You get {(total_protein/recommand_protein*100):.1f} % of your daily protein from beverages.'
    if select_sugar:
        recommand_sugar = (current_user.user_weight*10+current_user.user_height*6.25-current_user.user_age*5+F)*0.05
        if recommand_sugar/2 < total_sugar:
            sugar_suggestion = ('The sugar you intake from the beverages has exceeded half of your daily need! '
                                 'Please control your beverages intake.')
        else:
            sugar_suggestion = f'You get {(total_sugar/recommand_sugar*100):.1f} % of your daily energy from beverages.'
    if select_caffeine:
        recommand_caffeine = 400
        caffeine_suggestion = f'You get {(total_caffeine/recommand_caffeine*100):.1f} % of your daily caffeine intake recommandation from beverages.'

    # 将计算结果传递给模板

    return render_template('result.html',
                           select_water=select_water, total_water=total_water,
                           select_energy=select_energy, total_energy=total_energy,
                           select_protein=select_protein, total_protein=total_protein,
                           select_sugar=select_sugar, total_sugar=total_sugar,
                           select_caffeine=select_caffeine, total_caffeine=total_caffeine,
                           water_suggestion=water_suggestion,energy_suggestion=energy_suggestion,protein_suggestion=protein_suggestion,
                           sugar_suggestion=sugar_suggestion,caffeine_suggestion=caffeine_suggestion
    )



@BP.route('/logout')
@login_required
def logout():
    logout_user()
    picture()
    return redirect(url_for('start.index'))
