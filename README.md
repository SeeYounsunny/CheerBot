# MBTI 아침 응원 봇

해커톤용 Telegram 봇입니다. 팀원이 MBTI를 등록하면, 평일 아침 9시(KST)에 오늘의 컨디션 히어로를 뽑아 그룹 채팅에 응원 메시지를 보냅니다.

→ 팀원용 사용 방법은 **[봇 사용법](#봇-사용법)** 섹션을 참고하세요.

## 봇 사용법

AI BM 팀 해커톤용 Telegram 봇입니다. 팀 단톡방에 초대해 두면, 멤버가 MBTI를 등록하고 **평일 아침**에 오늘의 컨디션 히어로를 뽑아 응원 메시지를 보냅니다.

> **중요:** 이 봇은 ChatGPT처럼 **무엇이든 물어보면 답해 주는 Q&A 챗봇이 아닙니다.** `/mbti`, `/chatid` 같은 **슬래시 명령**에만 반응하고, 그 외 일반 메시지(“안녕”, “오늘 뭐 해?”, “코드 짜줘” 등)에는 **답하지 않습니다.**

### 이 봇이 하는 일 / 하지 않는 일

**하는 일**

- `/mbti` — 팀원 MBTI 등록·변경
- `/chatid` — 현재 채팅방 ID·유형 확인 (배포 설정용)
- **평일 아침** `CHEER_TIME`(기본 `09:00` KST)에 오늘의 컨디션 히어로를 뽑아 **설정된 그룹 채팅**(`TELEGRAM_CHAT_ID`)으로 응원 메시지 전송

**하지 않는 일**

- 자유 대화, 잡담, 일반 질문에 대한 답변
- 슬래시 명령 없이 보낸 메시지에 대한 응답
- 주말(토·일) 자동 응원 — 평일(월~금)만 동작

### 명령어 표

| 명령 | 설명 | 예시 |
|------|------|------|
| `/mbti` | MBTI 등록/변경 | `/mbti INFP` |
| `/chatid` | 현재 채팅방 ID 확인 | `/chatid` |

이 두 가지 명령만 지원합니다. 그룹·1:1 채팅 모두에서 사용할 수 있지만, 아침 응원은 `TELEGRAM_CHAT_ID`로 지정한 **그룹**으로만 갑니다.

### MBTI 등록 방법

1. **봇을 단톡방에 초대**하고, 메시지를 보낼 수 있는 권한을 줍니다.
2. 단톡방에서 **`/mbti TYPE`** 을 입력합니다. (예: `/mbti INFP`)
3. **16가지 MBTI**만 허용합니다: INTJ, INTP, ENTJ, ENTP, INFJ, INFP, ENFJ, ENFP, ISTJ, ISFJ, ESTJ, ESFJ, ISTP, ISFP, ESTP, ESFP
4. 이미 등록한 사람이 다시 `/mbti`를 보내면 **새 타입으로 덮어씁니다.**
5. 등록이 완료되면 아래처럼 확인 메시지가 옵니다.

```
✅ 홍길동 님의 MBTI가 INFP로 등록됐어요!
```

타입 없이 `/mbti`만 보내면 `사용법: /mbti INFP (16가지 MBTI 중 하나)` 안내가, 잘못된 타입이면 `올바른 MBTI 타입이 아니에요. 예: INFP, ENTJ (16가지)` 안내가 돌아옵니다.

### 아침 응원

- **언제:** 평일(월~금) **`CHEER_TIME`** (기본 `09:00`, KST). 환경 변수로 변경 가능 (예: `09:30`).
- **어디로:** Railway Variables의 `TELEGRAM_CHAT_ID`에 설정한 그룹 채팅.
- **누구를:** 그날 **요일별 MBTI 가중치**로 각 등록 멤버에게 점수를 매긴 뒤, 최고점 멤버를 **오늘의 히어로**로 선정합니다. 동점이면 무작위로 한 명을 고릅니다.
- **조건:** `/mbti`로 **1명 이상** 등록되어 있어야 합니다. 등록자가 없으면 그날은 건너뜁니다.

| 요일 | 가산 문자 | 의미 (예시) |
|------|-----------|-------------|
| 월 | E, J | 외향·판단형에 유리한 날 |
| 화 | T, S | 사고·감각형에 유리한 날 |
| 수 | N, E | 직관·외향형에 유리한 날 |
| 목 | F, I | 감정·내향형에 유리한 날 |
| 금 | P, E | 인식·외향형에 유리한 날 |

멤버 MBTI에 해당 문자가 있을 때마다 **+1점** (최대 2점). 히어로 MBTI 유형에 따라 응원 문구 톤도 달라집니다 (ENFP/ENTP → 아이디어·에너지, INTJ/INTP → 깊은 사고, 등).

```
[월요일 09:00]
🌅 오늘의 아침 응원!

오늘 가장 컨디션이 좋을 것 같은 사람은...
✨ @alice (ENFP) ✨

오늘도 아이디어 폭발할 것 같아요! 팀의 에너지가 되어주세요 🔥

화이팅! 💪
```

### 자주 묻는 질문 (FAQ)

**Q. 봇한테 뭐든 물어봐도 답해 주나요?**  
A. 아니요. 위 [명령어 표](#명령어-표)의 `/mbti`, `/chatid`만 처리합니다.

**Q. `/mbti`를 쳤는데 봇이 안 답해요.**  
A. 아래를 순서대로 확인하세요.
- Railway(또는 로컬)에서 봇 프로세스가 **실행 중**인지 (`TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` Variables 설정)
- 봇이 **단톡방에 초대**되어 있고, **메시지 보내기 권한**이 있는지
- **`/mbti INFP`** 처럼 **슬래시(/)로 시작**하는 명령인지 (일반 텍스트 “mbti INFP”는 동작하지 않음)
- 같은 토큰으로 로컬·Railway를 **동시에** 돌리고 있지 않은지 (409 충돌)

**Q. MBTI를 잘못 입력했어요.**  
A. 올바른 4글자 타입으로 **`/mbti`를 다시** 보내면 덮어씁니다. (예: `/mbti ENTJ`) 소문자 `infp`도 자동으로 대문자로 처리됩니다.

**Q. 아침 응원이 안 와요.**  
A. 주말이 아닌지, 최소 1명이 `/mbti`로 등록했는지, `TELEGRAM_CHAT_ID`가 응원을 받을 그룹 ID와 일치하는지 확인하세요. 그룹 ID는 `/chatid`로 확인할 수 있습니다.

## 사전 준비

### 1. BotFather에서 봇 생성

1. Telegram에서 [@BotFather](https://t.me/BotFather) 대화
2. `/newbot` → 이름·username 설정
3. 발급된 **Bot Token** 복사

### 2. 그룹 채팅 ID 확인

1. 팀 그룹에 봇 초대
2. 봇에게 메시지 보낼 수 있도록 권한 부여
3. 채팅 ID 확인: 그룹에서 `/chatid` 실행 (또는 [@getidsbot](https://t.me/getidsbot) 등)
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

### 3. 서비스 유형 (중요)

이 봇은 **HTTP API 서버가 아니라** Telegram **long polling** 프로세스입니다.

- **권장:** Railway 서비스 설정에서 유형이 **Worker**인지 확인합니다. `Procfile`의 `worker: python app.py`가 사용됩니다.
- **Web 서비스로 배포된 경우:** Railway는 `PORT`에서 헬스 체크를 기대합니다. `app.py`는 `PORT`가 설정되면 백그라운드에서 `GET /` → `ok` 응답을 열어 배포가 통과하도록 합니다. polling은 그대로 동작합니다.

`railway.toml`에 `startCommand`를 두지 않습니다. `startCommand`가 있으면 Procfile의 `worker:`를 덮어써서 Web 전용으로 뜨고, `PORT` 미바인딩으로 **Application failed to respond** / 재시작 루프가 날 수 있습니다.

### 4. 배포 확인

1. **Deployments** → 최신 배포 **View Logs**
2. 정상 로그 예:
   - `CheerBot starting`
   - `Health check HTTP server listening` (Web + `PORT` 설정 시) 또는 `health HTTP server skipped` (Worker)
   - `Webhook cleared; polling mode active`
   - `Starting MBTI cheer bot (polling mode)...`
3. Telegram 그룹에서 `/mbti ENFP` 테스트

### 5. 문제 해결 (Troubleshooting)

| 증상 | 원인 | 조치 |
|------|------|------|
| `Missing required environment variable: TELEGRAM_BOT_TOKEN` | Variables 미설정 | Railway **Variables**에 토큰·채팅 ID 추가 후 재배포 |
| `Application failed to respond` / 배포 직후 종료 | Web 서비스인데 `PORT` 미사용 | Worker로 전환하거나, 최신 `app.py`(PORT 헬스 서버)로 재배포 |
| `Conflict: terminated by other getUpdates` (409) | 같은 토큰으로 로컬 + Railway 동시 polling | 로컬 `python app.py` 중지, Railway만 실행 |
| 빌드는 되는데 봇이 무반응 | 잘못된 `TELEGRAM_CHAT_ID` 또는 그룹 권한 | 그룹에서 `/chatid`로 ID 확인, 봇에 메시지 권한 부여 |
| `Invalid CHEER_TIME` | `CHEER_TIME` 형식 오류 | `HH:MM` (예: `09:00`) |

배포 로그 일부(빌드 + 런타임 30줄)를 붙여 주시면 추가로 짚을 수 있습니다.

### 6. Railway vs Vercel

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
