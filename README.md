# MBTI 아침 응원 봇

해커톤용 Telegram 봇입니다. 팀원이 MBTI를 등록하면, 평일 아침 9시(KST)에 오늘의 컨디션 히어로를 뽑아 그룹 채팅에 응원 메시지를 보냅니다.

## 기능

- `/mbti INFP` — MBTI 등록/수정 (16타입 검증)
- 평일 09:00 KST — 요일별 MBTI 가중치로 히어로 선정 후 응원 메시지 전송

## 사전 준비

### 1. BotFather에서 봇 생성

1. Telegram에서 [@BotFather](https://t.me/BotFather) 대화
2. `/newbot` → 이름·username 설정
3. 발급된 **Bot Token** 복사

### 2. 그룹 채팅 ID 확인

1. 팀 그룹에 봇 초대
2. 봇에게 메시지 보낼 수 있도록 권한 부여
3. 채팅 ID 확인 (예시):
   - [@userinfobot](https://t.me/userinfobot) 또는 [@getidsbot](https://t.me/getidsbot)을 그룹에 추가해 ID 확인
   - 그룹 ID는 보통 `-100xxxxxxxxxx` 형태

### 3. 환경 변수

```bash
cp .env.example .env
```

`.env` 편집:

```env
TELEGRAM_BOT_TOKEN=123456:ABC...
TELEGRAM_CHAT_ID=-1001234567890
CHEER_TIME=09:00
```

## 로컬 실행

Python 3.11+ 필요.

```bash
cd /Users/1109239/CheerBot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

그룹 채팅에서 `/mbti ENFP` 등으로 등록한 뒤, 스케줄러가 설정한 시간에 응원 메시지가 전송됩니다.

## 프로젝트 구조

```
├── app.py           # 봇 진입점, /mbti 핸들러
├── scheduler.py     # APScheduler (Asia/Seoul)
├── mbti_logic.py    # MBTI 검증, 요일별 점수, 히어로 선정
├── messages.py      # 응원 문구 템플릿
├── storage.py       # data/members.json 읽기/쓰기
├── data/members.json
├── requirements.txt
└── .env.example
```

## 요일별 가중치 (평일)

| 요일 | 가산 문자 |
|------|-----------|
| 월 | E, J |
| 화 | T, S |
| 수 | N, E |
| 목 | F, I |
| 금 | P, E |

각 멤버 MBTI에 해당 문자가 있으면 +1점, 최고점 동점 시 무작위 선택.

## 데이터

`data/members.json` — Telegram user ID를 키로 저장합니다. 재등록 시 덮어씁니다.
