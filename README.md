# 잡코인 급상승 예측 시스템

업비트 API를 이용한 코인 데이터 수집 및 학습

## 순서
1. coin_selector.py
2. coin_collector.py
3. coin_preproc.py
4. coin_train.ipynb
5. coin_predict.py


## 1. coin_selector.py

타겟 코인 선정

* 업비트 API로 모든 코인 데이터를 받아와 조건에 맞는 코인을 선별
* 선정 기준 : 원화 마켓만, 가격이 낮음, 거래량이 적음

## 2. coin_collector.py

타겟 코인 데이터 수집

* 업비트 API로 타겟 코인의 월, 주, 일, 분(240/60) 별 데이터 수집
* 수집 데이터의 시간 간격이 모두 동일한지 검증

## 3. coin_preproc.py

1. 결측치 제거 - 2017년도에 데이처가 며칠 빠져있어서 그 이전까지 삭제
2. `change_rate`, `change_trade_rate`(어제 거래량 분의 오늘) ,`price_diff`(고가를 저가로 나눈 비율)
3. N,M을 바꿔가면 ARIMA로 일수 병렬화
4. 각 행에 맞는 정답 y를 이진분류로 생성

N,M,R을 조절하면서 전처리
* N: 예측을 위한 현재부터 N일 전까지 기간
* M: 현재로부터 예측하는 기간
* R: 현재로부터 M일 이후까지 가격이 몇배 증가하는지
* 파일 이름 형식 - {type}\_{N}_{M}_{R}.csv

## 4. coin_train.ipynb

학습은 랜덤 포레스트로 진행

## 5. coin_predict.py

서버에 배포해서 캔들이 업데이트 될때마다 실행시키면 됨