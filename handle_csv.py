import pandas as pd
import numpy as np
from joblib import load
from sklearn.preprocessing import LabelEncoder

class Datasheet:
    def __init__(self, file):
        self.file = file

    def compute(self):
        data = pd.read_csv(self.file)
        expe = data.copy()

        le = LabelEncoder()
        le.fit(data.sex.drop_duplicates())
        data.sex = le.transform(data.sex)

        le.fit(data.smoker.drop_duplicates())
        data.smoker = le.transform(data.smoker)

        le.fit(data.region.drop_duplicates())
        data.region = le.transform(data.region)

        predict_list = []

        model = load('random_forest_regressor.joblib')

        for row in data.index:
            df=pd.DataFrame(data.iloc[row,:]).T
            pred_val = model.predict(df)
            predict_list.append(np.exp(pred_val[0]))

        res_df = pd.DataFrame(predict_list,columns=['expenses'])

        expe['expenses'] = res_df['expenses']
        expe.to_csv('\\Users\\Kartheek\\Desktop\\env\\insurance_final\\static\\expenses.csv', index=False)