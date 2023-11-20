import pandas as pd
from joblib import dump, load
import json
import requests
import datetime
import os
import coin_preproc as cp


model_path = "coin/model/model_100_18_days_2_0_1_4_2_12_.pkl"
model = load(model_path)
coins=pd.read_csv("coin/target_coins.csv")["market"]

TYPE = "days"
A=2
B=0
C=1
N=4
M=2
R=1.2


def req(url):
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    return pd.DataFrame(json.loads(response.text))


def req_data(coins):
    total = []
    y_pred=pd.DataFrame()
    y_true=pd.DataFrame()
    true_count=0
    TP=0
    TN=0
    FP=0
    FN=0
    for coin in coins:
        df_coin = req(f"https://api.upbit.com/v1/candles/{TYPE}?market={coin}&count={N*10}")
        df_pre_coin = cp.make_X1(df_coin,A,B,C)
        X = cp.make_X2(df_pre_coin, N)
        y = cp.make_y(X['change_rate0']+1, M,R)
        y_true[coin] = y
        y_pred[coin] = model.predict(X)
        total.append(X.loc[0:0])
        true_count += (y_true[coin].loc[M:]==y_pred[coin].loc[M:]).sum()
        for i in range(M,len(y_true)):
            if y_pred[coin][i] == 1 and y_true[coin][i] == 1:
                TP+=1
            if y_pred[coin][i] == 0 and y_true[coin][i] == 0:
                TN+=1
            if y_pred[coin][i] == 1 and y_true[coin][i] == 0:
                FP+=1
            if y_pred[coin][i] == 0 and y_true[coin][i] == 1:
                FN+=1    
    df_total = pd.concat(total, axis=0,ignore_index=True)
    df_total['market'] = coins
    print("------------data------------")
    print(df_total)
    print("-----------y_pred-----------")
    print(y_pred)
    print("-----------y_true-----------")
    print(y_true)
    print("-----------score-----------")
    print("TP:",TP,"TN:",TN,"FP:",FP,"FN:",FN)
    print("정확도:",(TP+TN)/(TP+TN+FP+FN))
    print("정밀도:",(TP)/(TP+FP))
    
        



if __name__ == "__main__":
    df_coins = pd.read_csv("coin/target_coins.csv")
    coins=df_coins["market"]
    # print(coins)
    
    req_data(coins)