import os
import time
from datetime import datetime, timedelta
import pandas
import json
import requests


# 필요한 폴더 생성
folder_paths = ["minutes/60","minutes/240","days","weeks","months"]
for path in folder_paths:
    if not os.path.exists("coin/"+path):
        os.makedirs("coin/"+path)

def req(url):
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    return pandas.DataFrame(json.loads(response.text))

DATES=["2023-10-10 14:30:00"]
PATH=folder_paths[3]
COUNT=200

for i in range(20):
    date_format = "%Y-%m-%d %H:%M:%S"
    next_date = datetime.strptime(DATES[i], date_format) - timedelta(weeks=200)
    DATES.append(next_date.strftime(date_format))


def collectCoin(start_coin_index = 0):
    target_coins = pandas.read_csv("target_coins.csv")
    coins=target_coins["market"].tolist()
    request_count=0 # 업비트 API 초당 5번, 분당 100번 요청 가능
    coin_index = start_coin_index
    for coin in coins[start_coin_index:]: 
        df = pandas.DataFrame()
        for date in DATES:
            # 코인 데이터 요청
            res = req(f"https://api.upbit.com/v1/candles/{PATH}?market={coin}&to={date}&count={COUNT}")
            df = pandas.concat([df,res])

            # 요청 카운트 계산(5번 연속으로 요청했다면 3초 쉼)
            request_count+=1
            if(request_count % 5 == 0):
                time.sleep(2)

            # 과거 날짜의 데이터가 더이상 없다면 다음 코인으로
            if df.shape[0] <COUNT :
                break
        
        df.to_csv(f"coin/{PATH}/{coin}.csv", index=False)
        print(coin_index, PATH, coin, "코인 로딩 완료")
        coin_index+=1

collectCoin()

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