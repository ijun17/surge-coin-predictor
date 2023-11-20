import os
import time
from datetime import datetime, timedelta
import pandas
import json
import requests


# 필요한 폴더 생성
BASE_PATH = "coin/raw/"
TYPES = ["minutes/60","minutes/240","days","weeks"]
[os.makedirs(BASE_PATH + path) for path in TYPES if not os.path.exists(BASE_PATH + path)]

def req(url):
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    return pandas.DataFrame(json.loads(response.text))


def collectCoin(coins,type):
    COUNT=200
    # REST API 요청 수 제한은 IP 단위로 측정됩니다. 초당 10회
    for i,coin in enumerate(coins): 
        df = pandas.DataFrame()
        date = "2023-10-10T14:30:00"
        while True:
            # 코인 데이터 요청
            res = req(f"https://api.upbit.com/v1/candles/{type}?market={coin}&to={date}&count={COUNT}")
            df = pandas.concat([df,res])
            # time.sleep(0.1)# 초당 10회
            if res.shape[0] <COUNT :
                break
            date = res["candle_date_time_utc"].iloc[-1]
        df.to_csv(BASE_PATH+type+"/"+coin+".csv", index=False)
        print(i, type, coin, "코인 로딩 완료")



def verifyCoin(coins,type):
    for i,coin in enumerate(coins):
        date_format = "%Y-%m-%dT%H:%M:%S"  # 날짜 형식 지정
        df_coin = pandas.read_csv(BASE_PATH+type+"/"+coin+".csv")
        times = df_coin["candle_date_time_utc"]
        prev_date = datetime.strptime(times[0], date_format)
        TIME_DELTA = prev_date-datetime.strptime(times[1], date_format)
        for j,t in enumerate(times[1:]):
            cur_date = datetime.strptime(t, date_format)
            td = prev_date - cur_date
            if td != TIME_DELTA:
                print("Missing:",coin,"At",j,"count",int(td/TIME_DELTA-1),"time",t)
            prev_date=cur_date
        print(i,coin,"검증완료 to",prev_date)



if __name__ == "__main__":
    df_coins = pandas.read_csv("coin/target_coins.csv")
    coins=df_coins["market"]
    # collectCoin(coins[52:], TYPES[1])
    verifyCoin(coins, TYPES[1])


"""
0 KRW-SNT 코인 로딩 완료
1 KRW-XEM 코인 로딩 완료
2 KRW-STEEM 코인 로딩 완료
3 KRW-XLM 코인 로딩 완료
4 KRW-ARDR 코인 로딩 완료
5 KRW-GRS 코인 로딩 완료
6 KRW-ADA 코인 로딩 완료
7 KRW-POWR 코인 로딩 완료
8 KRW-ICX 코인 로딩 완료
9 KRW-EOS 코인 로딩 완료
10 KRW-ONT 코인 로딩 완료
11 KRW-ZIL 코인 로딩 완료
12 KRW-POLYX 코인 로딩 완료
13 KRW-BAT 코인 로딩 완료
14 KRW-IOST 코인 로딩 완료
15 KRW-CVC 코인 로딩 완료
16 KRW-IQ 코인 로딩 완료
17 KRW-IOTA 코인 로딩 완료
18 KRW-HIFI 코인 로딩 완료
19 KRW-ONG 코인 로딩 완료
20 KRW-UPP 코인 로딩 완료
21 KRW-ELF 코인 로딩 완료
22 KRW-KNC 코인 로딩 완료
23 KRW-THETA 코인 로딩 완료
24 KRW-QKC 코인 로딩 완료
25 KRW-MOC 코인 로딩 완료
26 KRW-TFUEL 코인 로딩 완료
27 KRW-MANA 코인 로딩 완료
28 KRW-ANKR 코인 로딩 완료
29 KRW-AERGO 코인 로딩 완료
30 KRW-HBAR 코인 로딩 완료
31 KRW-MED 코인 로딩 완료
32 KRW-MLK 코인 로딩 완료
33 KRW-VET 코인 로딩 완료
34 KRW-CHZ 코인 로딩 완료
35 KRW-DKA 코인 로딩 완료
36 KRW-HIVE 코인 로딩 완료
37 KRW-KAVA 코인 로딩 완료
38 KRW-AHT 코인 로딩 완료
39 KRW-BORA 코인 로딩 완료
40 KRW-JST 코인 로딩 완료
41 KRW-CRO 코인 로딩 완료
42 KRW-SXP 코인 로딩 완료
43 KRW-HUNT 코인 로딩 완료
44 KRW-PLA 코인 로딩 완료
45 KRW-GLM 코인 로딩 완료
46 KRW-SSX 코인 로딩 완료
47 KRW-META 코인 로딩 완료
48 KRW-FCT2 코인 로딩 완료
49 KRW-SAND 코인 로딩 완료
50 KRW-HPO 코인 로딩 완료
51 KRW-PUNDIX 코인 로딩 완료
52 KRW-FLOW 코인 로딩 완료
53 KRW-MATIC 코인 로딩 완료
54 KRW-1INCH 코인 로딩 완료
55 KRW-ALGO 코인 로딩 완료
56 KRW-CELO 코인 로딩 완료
57 KRW-GMT 코인 로딩 완료
58 KRW-SUI 코인 로딩 완료
59 KRW-GRT 코인 로딩 완료
60 KRW-BLUR 코인 로딩 완료
61 KRW-IMX 코인 로딩 완료
"""