# MBTI 아침 응원 봇

해커톤용 Telegram 봇입니다. 팀원이 MBTI를 등록하면, 평일 아침 9시(KST)에 오늘의 컨디션 히어로를 뽑아 그룹 채팅에 응원 메시지를 보냅니다.

## 기능

- `/mbti INFP` — MBTI 등록/수정 (16타입 검증)
- 평일 `CHEER_TIME` KST — 요일별 MBTI 가중치로 히어로 선정 후 응원 메시지 전송

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

## 로컬 실행 (polling)

Python 3.11+ 필요.

```bash
cd CheerBot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

그룹 채팅에서 `/mbti ENFP` 등으로 등록한 뒤, 스케줄러가 설정한 시간에 응원 메시지가 전송됩니다.

> **주의:** 같은 봇 토큰으로 polling을 두 곳에서 동시에 실행하면 Telegram 업데이트가 충돌합니다(409). Railway에 배포한 뒤에는 Railway 인스턴스만 실행하세요.

## Railway 배포

이 프로젝트는 **Railway 전용**입니다. `app.py`가 polling + APScheduler로 상시 실행됩니다. Vercel webhook 방식은 사용하지 않습니다.

### 1. GitHub 연결

1. [railway.app](https://railway.app) 로그인
2. **New Project** → **Deploy from GitHub repo**
3. 저장소 **SeeYounsunny/CheerBot** 선택, 브랜치 **main**
4. push 시 **자동 재배포** (기본 Git 연동)

### 2. 환경 변수 (Variables)

서비스 → **Variables** 탭에서 추가:

| 변수 | 설명 | 예시 |
|------|------|------|
| `TELEGRAM_BOT_TOKEN` | BotFather 토큰 | `123456:ABC...` |
| `TELEGRAM_CHAT_ID` | 그룹 채팅 ID | `-1001234567890` |
| `CHEER_TIME` | 평일 응원 시각 (KST, HH:MM) | `09:00` |

### 3. 배포 확인

1. **Deployments** → 최신 배포 **View Logs**
2. 로그에 `Webhook cleared; polling mode active` 및 `Starting MBTI cheer bot` 가 보이면 정상
3. Telegram 그룹에서 `/mbti ENFP` 테스트

### 4. Railway vs Vercel

- **Railway:** `python app.py` polling + 스케줄러 (이 저장소의 방식)
- **Vercel webhook:** 이 저장소에는 포함하지 않음. 과거 webhook을 등록했다면 Railway 시작 시 `deleteWebhook`으로 제거됩니다.

### 데이터 저장

`data/members.json`에 멤버가 저장됩니다. Railway 볼륨을 붙이지 않으면 재배포 시 파일이 초기화될 수 있습니다. 해커톤 데모 후에는 Volume 또는 외부 DB 연동을 권장합니다.

## 프로젝트 구조

```
├── app.py              # Railway 진입점 (polling)
├── Procfile            # worker: python app.py
├── railway.toml        # Nixpacks 빌드 / start 명령
├── runtime.txt         # Python 3.11
├── handlers.py         # /mbti 공통 로직
├── cheer.py            # 아침 응원 로직
├── scheduler.py        # APScheduler (KST)
├── mbti_logic.py       # MBTI 검증, 요일별 점수, 히어로 선정
├── messages.py         # 응원 문구 템플릿
├── storage.py          # members.json 읽기/쓰기
├── telegram_client.py  # sendMessage API
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
