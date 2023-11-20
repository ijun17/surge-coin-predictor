import pandas
import json
import requests

def req(url):
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    return pandas.DataFrame(json.loads(response.text))

# 코인 티커로 코인 선별
def selectTargetCoins():
    # 모든 코인 데이터를 서버에서 받아옴
    all_coins = req("https://api.upbit.com/v1/market/all?isDetails=false")
    all_coins_ticker = req("https://api.upbit.com/v1/ticker?markets="+all_coins["market"].str.cat(sep=','))

    df = all_coins_ticker[["market","low_price","acc_trade_price_24h"]]
    df = df.astype({'low_price': "int64", 'acc_trade_price_24h': "int64"})

    filter0 = (df["market"].str.contains("KRW"))            # 원화 마켓만
    filter1 = (df["low_price"]<1000) & (df["low_price"]>5)  # low_price : 거래일 동안 가장 낮은 거래액
    filter2 = (df["acc_trade_price_24h"]<7000000000)        # acc_trade_price_24h: 24지난 24시간 동안 누적거래량
    df = df[filter0 & filter1 & filter2]

    # 저장 및 완료
    df.to_csv("coin/target_coins.csv", index=False)
    print("타켓 코인 선별 완료")


if __name__ == "__main__":
    selectTargetCoins()