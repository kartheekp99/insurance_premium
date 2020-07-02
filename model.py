import pandas as pd

data=pd.read_csv("insurance_mod.csv")


# Data Cleaning by removing obscure data
ma=data['age'].mean()
mb=data['bmi'].mean()
me=data['expenses'].mean()

junk = data[((data['age']<ma)&(data['smoker']=='no')&(data['children']<2)&(data['bmi']<=mb))&(data['expenses']>=me)]
data = data.drop(junk.index)

bad = data[((data['age']<ma)&(data['smoker']=='no')&(data['children']<2))&(data['expenses']>me)]
data = data.drop(bad.index)

import numpy as np
data['expenses'] = np.log(data['expenses'])



# Label ENcoding Categorical Columns
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
le.fit(data.sex.drop_duplicates())
data.sex = le.transform(data.sex)

le.fit(data.smoker.drop_duplicates())
data.smoker = le.transform(data.smoker)

le.fit(data.region.drop_duplicates())
data.region = le.transform(data.region)


# Independent and Dependent variables
x = data.drop('expenses',axis=1)
y = data['expenses']



# Splitting Training and testing data
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 0)


# Running Random Forest Regressor after Hyperparameter Tuning
from sklearn.ensemble import RandomForestRegressor 
model = RandomForestRegressor(
                max_depth= 50,
                min_samples_leaf= 10, 
                min_samples_split= 7, 
                n_estimators= 1200, 
                random_state= 42 )

model = model.fit(x_train, y_train)



# Calculating R Square
from sklearn.metrics import r2_score

y_pred_train = model.predict(x_train)
r2_score_train = r2_score(y_train, y_pred_train)

y_pred_test = model.predict(x_test)
r2_score_test = r2_score(y_test, y_pred_test)

print('R2_score (train): ', r2_score_train)
print('R2_score (test): ', r2_score_test)



#Saving the model
from joblib import dump
  
dump(model, 'random_forest_regressor.joblib')