from MainProject import App_Creation, db
import pandas as pd
from MainProject.drink_class import Drink
app = App_Creation()

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
        excel_file_path = 'MainProject/static/drinks data1.xlsx'
        df = pd.read_excel(excel_file_path)

        for i in range(df.shape[0]):

            drink = Drink(drink_name=df['Name'][i],
                          drink_water=float(df['Water/g'][i]),
                          drink_energy=float(df['Energy/kcal'][i]),
                          drink_protein=float(df['Protein/g'][i]),
                          drink_sugar=float(df['Sugars/g'][i]),
                          drink_caffeine=float(df['Caffeine/mg'][i]))
        # 将对象添加到会话
            db.session.add(drink)
        db.session.commit()
    app.run(debug=True, host='0.0.0.0', port=5001)
