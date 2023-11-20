import numpy
import pandas as pd
from imblearn.over_sampling import RandomOverSampler

RAW_PATH = "coin/raw/days/"
BASE_PATH = "coin/preprocessed/"
PATH = "days"


def make_X1(df, A,B,C):
    df_pre_coin = pd.DataFrame()
    if A>0:
        df_pre_coin["change_rate"] = df["change_rate"]
    if B>0:
        df_pre_coin["change_trade_rate"] = df["candle_acc_trade_volume"]/df["candle_acc_trade_volume"].shift(-1)
    if C>0:
        df_pre_coin["price_diff"] = df["high_price"]/df["low_price"]
    return df_pre_coin

def make_X2(df,N):
    result_df = pd.DataFrame()
    for n in range(N):
        for column in df.columns:
            result_df[column+str(n)] = df[column].shift(-n).reset_index(drop=True)[:-N+1]
    return result_df

def make_y(rates,M,R):
    y = pd.Series([0]*len(rates))
    for j in range(M,len(rates)):
        if(rates.iloc[j-M:j].product()>=R):
            y[j]=1
        # temp = 1
        # for k in range(1,M+1):
        #     temp *= rates[j-k]
        #     if temp >= R:
        #         y[j] = 1
        #         break
    return y


"""
전처리
A:Boolean - 데이터에 "change_rate"를 포함 시킬지
B:Boolean - 데이터에 "candle_acc_trade_volume"를 포함 시킬지
C:Booleam - 데이터에 "price_diff"를 포함 시킬지
N:Integer - 예측을 위한 현재부터 N일 전까지 기간
M:Integer - 현재로부터 예측하는 기간
R:Float - 증가율
"""
def preprocess(coins,A,B,C,N,M,R):
    total=[]
    for i,coin in enumerate(coins):
        df_coin = pd.read_csv(RAW_PATH+coin+".csv")
        df_pre_coin = make_X1(df_coin,A,B,C)
        X = make_X2(df_pre_coin, N)
        y = make_y(df_pre_coin["change_rate"]+1, M,R)
        X['y'] = y[:-N-1].astype(int)
        total.append(X[M:-1])
    df_total = pd.concat(total, axis=0,ignore_index=True)
    df_total.to_csv(BASE_PATH+PATH+f"/{PATH.replace('/', '')}_{A}_{B}_{C}_{N}_{M}_{int(R*10)}_.csv", index=False)
    print(df_total.info())
    print("y==1 비율",(df_total['y']==1).mean())


if __name__ == "__main__":
    df_coins = pd.read_csv("coin/target_coins.csv")
    coins=df_coins["market"].tolist()

    preprocess(coins,2,0,1,4,2,1.2)