import warnings
import pandas as pd
from joblib import dump, load
import json
import requests
from datetime import datetime
import coin_preproc as cp

warnings.filterwarnings("ignore")

BASE_PATH = "coin/model/"
model_name = "extratree_15_40_17.pkl"
model = load(BASE_PATH+model_name)
coins=pd.read_csv("coin/target_coins.csv")["market"]

TYPE = "days"
A=0
B=0
C=1
N=15
M=20
R=1.5


def req(url):
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    return pd.DataFrame(json.loads(response.text))


def saveData(coins, y_true, y_pred,ACCURACY, PRECISION):
    coins_json = json.dumps(coins.to_list())
    y_true_json = json.dumps(y_true.to_dict(orient='list'))
    y_pred_json = json.dumps(y_pred.to_dict(orient='list'))

    js_text = f"const coins = {coins_json}, y_true={y_true_json}, y_pred={y_pred_json},N={N},M={M},R={R},DATE='{datetime.now()}',ACCURACY={ACCURACY},PRECISION={PRECISION};"
    with open("web/coins/data.js", 'w') as file:
        file.write(js_text)

def req_data(coins):
    TP,TN,FP,FN=0,0,0,0
    COUNT = 200
    total = []
    y_pred=pd.DataFrame({coin: [-1] * COUNT for coin in coins})
    y_true=pd.DataFrame({coin: [-1] * COUNT for coin in coins})
    for coin in coins:
        df_coin = req(f"https://api.upbit.com/v1/candles/{TYPE}?market={coin}&count={COUNT}")
        X = cp.make_X2(cp.make_X1(df_coin,A,B,C), N)
        trues = cp.make_y(df_coin["change_rate"].reset_index(drop=True)[:-N]+1, M,R)
        y_true[coin][:len(trues)] = trues
        predictions = model.predict(X)
        y_pred[coin][:len(predictions)] = predictions
        total.append(X.loc[0:0])
        val_pred,val_true = y_pred[coin][M:len(predictions)],y_true[coin][M:len(predictions)]
        TP += ((val_pred == 1)&(val_true == 1)).sum()
        TN += ((val_pred == 0)&(val_true == 0)).sum()
        FP += ((val_pred == 1)&(val_true == 0)).sum()
        FN += ((val_pred == 0)&(val_true == 1)).sum()
    df_total = pd.concat(total, axis=0,ignore_index=True)
    df_total['market'] = coins
    print("TP:",TP,"TN:",TN,"FP:",FP,"FN:",FN)
    ACCURACY=(TP+TN)/(TP+TN+FP+FN)
    PRECISION=-1 if TP+FP == 0 else (TP)/(TP+FP)
    print("정확도:",ACCURACY)
    print("정밀도:",PRECISION)
    #save data
    saveData(coins, y_true, y_pred,ACCURACY, PRECISION)



if __name__ == "__main__":
    df_coins = pd.read_csv("coin/target_coins.csv")
    coins=df_coins["market"]
    # print(coins)
    req_data(coins)

