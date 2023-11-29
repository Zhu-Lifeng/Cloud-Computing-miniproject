import pandas as pd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from MainProject.drink_class import Drink  # 确保正确导入你的 Drink 模型

# 创建一个临时的 Flask 应用和 SQLAlchemy 实例
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDB.sqlite'  # 替换为你的数据库 URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 使用你的 Excel 文件路径
excel_file_path = '/Users/yuhongye/Desktop/drinks data1.xls'

# 读取 Excel 文件
df = pd.read_excel(excel_file_path)

df['drink_caffeine'] = df['drink_caffeine'].fillna(0)

# 创建应用上下文
with app.app_context():
    # 遍历 DataFrame 行
    for _, row in df.iterrows():
        # 创建 Drink 对象
        drink = Drink(
            drink_name=row['drink_name'],
            drink_water=row['drink_water'],
            drink_energy=row['drink_energy'],
            drink_protein=row['drink_protein'],
            drink_sugar=row['drink_sugar'],
            drink_caffeine=row['drink_caffeine']
        )
        # 将对象添加到会话
        db.session.add(drink)

    # 提交会话到数据库
    db.session.commit()
