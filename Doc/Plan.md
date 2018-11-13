# Plan

## function
- [ ] **[main]** 사용자의 휴대폰이 문 가까이 가면 문이 자동으로 열린다.
  - 얼마나 가까이 가야 열리는지는 사용자가 조절 할 수 있다.
- [ ] 사용자가 원격으로 집 문을 열 수 있다.
- [ ] 사용자의 집 문 열고 닫힘 기록되고 알람이 온다.

# Implementation
## basic function
- [ ] Smart Phone이 IoT Device에 가까이 가면 자동 페어링 
  - Device 와 Phone간 rssi 신호세기 측정
- [ ] Smart Phone에서 Device에 open 요청
- [ ] Device에서 open 요청을 받음
- [ ] Device에서 서보모터를 작동해 문을 열음

## auth
- [ ] AWS에 open 인증 요청
- [ ] AWS에서 전송된 정보로 인증 확인
- [ ] AWS에서 Device로 인증 허가/불허 전송

## Data
- [ ] AWS DynamoDB에 사용자 등록
- [ ] AWS DynamoDB에 Device 등록
- [ ] AWS DynamoDB에 사용자와 Device 연결

## etc
- [ ] 집 내, 외부 구별에 따른 
