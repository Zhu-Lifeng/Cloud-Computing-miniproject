from flask_login import UserMixin

#from . import db
#以下数据需从数据库抓取
class User(UserMixin):#, db.Model):
    user_id="按数据库逻辑修改"
    user_email="按数据库逻辑修改"
    user_name = "按数据库逻辑修改"
    user_password="按数据库逻辑修改"
    user_weight= '按数据库逻辑修改'
    user_height="按数据库逻辑修改"
    user_age="按数据库逻辑修改"