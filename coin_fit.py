import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import os
from imblearn.combine import SMOTEENN

DATA_PATH = "coin/preprocessed/"
TYPE = "days"

data_path = "/kaggle/input/mycoin/coin_1_0_1_7_2_12_.csv"
df=pd.read_csv(data_path)

# 데이터셋의 X와 y가 있다고 가정
# X는 특성(feature), y는 타겟(label) 데이터
X = df.drop('y', axis=1)
y = df['y']

_X_train, _X_val, _y_train, _y_val = train_test_split(X, y, test_size=0.1, random_state=42)
sampler_train = SMOTEENN(sampling_strategy=0.5, random_state=42) 
X_train, y_train = sampler_train.fit_resample(_X_train, _y_train)
sampler_val = SMOTEENN(sampling_strategy=0.5, random_state=43) 
X_val, y_val = sampler_val.fit_resample(_X_val, _y_val)

print("1비율",(y_train==1).mean(), (y_val==1).mean())

def fit():
    EST = 100
    DEP = 20

    data_name = os.path.splitext(os.path.basename(data_path))[0]
    model_name = f"model_{EST}_{DEP}_"+data_name

    # 랜덤 포레스트 학습
    model = RandomForestClassifier(n_estimators=EST, max_depth=DEP, random_state=1)
    model.fit(X_train, y_train)
    print(model.score(X_val, y_val))