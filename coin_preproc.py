import numpy
import pandas as pd

RAW_PATH = "coin/raw/days/"
BASE_PATH = "coin/preprocessed/"
PATH = "days"

# 피쳐 만듦
def make_X1(df):
    df_pre_coin = pd.DataFrame()
    # df_pre_coin["change_rate"] = df["change_rate"].round(5)
#     df_pre_coin["change_trade_rate"] = (df["candle_acc_trade_volume"]/df["candle_acc_trade_volume"].shift(-1)).round(5)
#     df_pre_coin["candle_acc_trade_volume"] = df["candle_acc_trade_volume"].round(0)
    df_pre_coin["price_diff"] = (df["high_price"]/df["low_price"]).round(5)
    df_pre_coin["low_price_change_rate"] = df["low_price"]/df["low_price"].shift(-1).round(5)
#     df_pre_coin["high_price_change_rate"] = df["high_price"]/df["high_price"].shift(-1).round(5)
    return df_pre_coin[:-1]

# 데이터 N일 만큼 병렬화
def make_X2(df,N):
    result_df = pd.DataFrame()
    for n in range(N):
        for column in df.columns:
            result_df[column+str(n)] = df[column].shift(-n).reset_index(drop=True)[:-N+1]
    return result_df

# M일 안에 R배 증가하는지
def make_y(rates,M,R): 
    y = pd.Series([0]*len(rates))
    for j in range(M,len(rates)):
        temp = 1
        for k in range(1,M+1):
            temp *= rates[j-k]
            if temp >= R:
                y[j] = 1
                break
    return y


def preprocess(path, coins,N,M,R):
    total=[]
    for coin in coins:
        df_coin = pd.read_csv(path+coin+".csv")
        X = make_X2(make_X1(df_coin), N)
        change_rate = df_coin["change_rate"].reset_index(drop=True)[:-N+1]
        y = make_y(change_rate+1, M,R)
        X['y'] = y
        total.append(X[M:-1])
    df_total = pd.concat(total, axis=0,ignore_index=True)
    return df_total



if __name__ == "__main__":
    df_coins = pd.read_csv("coin/target_coins.csv")
    coins=df_coins["market"].tolist()

    df_total = preprocess("coin/raw/days/",coins,4,1,1.1)
    print(df_total.info())
    print("y==1 비율",(df_total['y']==1).mean())