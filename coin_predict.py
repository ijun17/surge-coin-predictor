import pandas as pd
from joblib import dump, load
import json
import requests
from datetime import datetime
import os
import coin_preproc as cp


BASE_PATH = "coin/model/"
model_name = "model_100_18_days_2_0_1_4_2_12_.pkl"
model = load(BASE_PATH+model_name)
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


def saveData(coins, y_true, y_pred,ACCURACY, PRECISION):
    coins_json = json.dumps(coins.to_list())
    y_true_json = json.dumps(y_true.to_dict(orient='list'))
    y_pred_json = json.dumps(y_pred.to_dict(orient='list'))

    js_text = f"const coins = {coins_json}, y_true={y_true_json}, y_pred={y_pred_json},N={N},M={M},R={R},DATE='{datetime.now()}',ACCURACY={ACCURACY},PRECISION={PRECISION};"
    # 파일을 쓰기 모드로 열기 (파일이 없으면 새로 생성됨)
    with open("web/data.js", 'w') as file:
        # 파일에 데이터 쓰기
        file.write(js_text)

def req_data(coins):
    total = []
    test = []
    trues = []
    y_pred=pd.DataFrame()
    y_true=pd.DataFrame()
    true_count=0
    TP=0
    TN=0
    FP=0
    FN=0
    COUNT = 100
    for coin in coins:
        df_coin = req(f"https://api.upbit.com/v1/candles/{TYPE}?market={coin}&count={COUNT}")
        df_pre_coin = cp.make_X1(df_coin,A,B,C)
        X = cp.make_X2(df_pre_coin, N)
        y = cp.make_y(X["change_rate0"]+1, M,R)
        y_true[coin] = y
        y_pred[coin] = model.predict(X)
        total.append(X.loc[0:0])
        test.append(X.iloc[M:])
        trues.append(y.iloc[M:])
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
    ACCURACY=(TP+TN)/(TP+TN+FP+FN)
    PRECISION=(TP)/(TP+FP)
    print("정확도:",ACCURACY)
    print("정밀도:",PRECISION)
    #save data
    saveData(coins, y_true, y_pred,ACCURACY, PRECISION)
    # save validation
    df_test = pd.concat(test, axis=0,ignore_index=True)
    df_trues = pd.concat(trues, axis=0,ignore_index=True)
    df_test['y'] = df_trues
    df_test.to_csv(BASE_PATH+"test_"+model_name+".csv", index=False)



if __name__ == "__main__":
    df_coins = pd.read_csv("coin/target_coins.csv")
    coins=df_coins["market"]
    # print(coins)
    req_data(coins)
