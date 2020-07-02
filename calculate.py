import pandas as pd
import numpy as np
from joblib import load

class Calculate:
    def __init__(self, age, sex, bmi, smoker, children, region):
        self.age=age
        self.bmi=bmi
        self.sex=sex
        self.smoker=smoker
        self.children=children
        self.region=region

    def calculate(self):
        data = pd.DataFrame([[ self.age, self.sex, self.bmi, self.smoker, self.children, self.region ]]
                            ,columns=['age', 'sex', 'bmi', 'children', 'smoker', 'region'])
        model = load('random_forest_regressor.joblib')
        val = round(np.exp(model.predict(data)[0]), 2)
        return val