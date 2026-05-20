# MBTI 아침 응원 봇

AI BM 팀용 Telegram 봇입니다. 팀원이 MBTI를 등록하면, 평일 아침 9시(KST)에 오늘의 컨디션 히어로를 뽑아 그룹 채팅에 응원 메시지를 보냅니다.

## 기능

| 기능 | 설명 |
|------|------|
| `/mbti` | 팀원 MBTI 등록·변경 |
| `/chatid` | 현재 채팅방 ID·유형 확인 (배포 설정용) |
| `/test` | 아침 응원 메시지 미리보기 (주말·스케줄 무시) |
| **평일 아침 응원** | `CHEER_TIME`(기본 `09:00` KST)에 히어로 선정 후 `TELEGRAM_CHAT_ID` 그룹으로 전송 |

> **중요:** 이 봇은 ChatGPT처럼 **무엇이든 물어보면 답해 주는 Q&A 챗봇이 아닙니다.** 위 **슬래시 명령**에만 반응하고, 그 외 일반 메시지에는 **답하지 않습니다.**

- **하는 일:** MBTI 등록, 채팅 ID 확인, 응원 미리보기, 평일(월~금) 자동 응원
- **하지 않는 일:** 자유 대화·잡담·일반 질문 응답, 주말(토·일) 자동 응원

## 봇 사용법

### 명령어

| 명령 | 설명 | 예시 |
|------|------|------|
| `/mbti` | MBTI 등록/변경 | `/mbti INFP` |
| `/chatid` | 현재 채팅방 ID 확인 | `/chatid` |
| `/test` | 오늘 기준 응원 메시지 미리보기 | `/test` |

그룹·1:1 채팅 모두에서 사용할 수 있지만, **아침 응원은 `TELEGRAM_CHAT_ID`로 지정한 그룹**으로만 전송됩니다.

### MBTI 등록 방법

1. **봇을 단톡방에 초대**하고, 메시지를 보낼 수 있는 권한을 줍니다.
2. 단톡방에서 **`/mbti TYPE`** 을 입력합니다. (예: `/mbti INFP`) — 채팅창에 `/`를 치면 Telegram이 명령 메뉴를 보여줍니다.
3. **16가지 MBTI**만 허용합니다: INTJ, INTP, ENTJ, ENTP, INFJ, INFP, ENFJ, ENFP, ISTJ, ISFJ, ESTJ, ESFJ, ISTP, ISFP, ESTP, ESFP
4. 이미 등록한 사람이 다시 `/mbti`를 보내면 **새 타입으로 덮어씁니다.**
5. 등록이 완료되면 확인 메시지가 옵니다.

```
✅ 홍길동 님의 MBTI가 INFP로 등록됐어요!
```

타입 없이 `/mbti`만 보내면 사용법 안내가, 잘못된 타입이면 `올바른 MBTI 타입이 아니에요. 예: INFP, ENTJ (16가지)` 안내가 돌아옵니다.

### `/test` 미리보기

`/test`는 **실제 그룹 전송 없이** 현재 등록 멤버 기준으로 아침 응원 메시지를 **바로** 보여 줍니다.

- 주말이어도 동작합니다 (스케줄·주말 스킵 무시).
- 메시지 앞에 `🧪 테스트 미리보기` 접두어가 붙습니다.
- 등록된 멤버가 없으면 `아직 등록된 팀원이 없어요. /mbti 로 MBTI를 등록해 주세요!` 가 표시됩니다.

### 아침 응원 (자동)

- **언제:** 평일(월~금) **`CHEER_TIME`** (기본 `09:00`, KST)
- **어디로:** `TELEGRAM_CHAT_ID`에 설정한 그룹 채팅
- **누구를:** 요일별 MBTI 가중치로 점수를 매긴 뒤 최고점 멤버를 **오늘의 히어로**로 선정 (동점이면 무작위)
- **조건:** `/mbti`로 **1명 이상** 등록되어 있어야 합니다

| 요일 | 가산 문자 | 의미 (예시) |
|------|-----------|-------------|
| 월 | E, J | 외향·판단형에 유리한 날 |
| 화 | T, S | 사고·감각형에 유리한 날 |
| 수 | N, E | 직관·외향형에 유리한 날 |
| 목 | F, I | 감정·내향형에 유리한 날 |
| 금 | P, E | 인식·외향형에 유리한 날 |

멤버 MBTI에 해당 문자가 있을 때마다 **+1점** (최대 2점). 히어로 MBTI 유형에 따라 응원 문구 톤도 달라집니다.

```
[월요일 09:00]
🌅 오늘의 아침 응원!

오늘 가장 컨디션이 좋을 것 같은 사람은...
✨ @alice (ENFP) ✨

오늘도 아이디어 폭발할 것 같아요! 팀의 에너지가 되어주세요 🔥

화이팅! 💪
```

## 프로젝트 구조

```
CheerBot/
├── app.py              # 진입점 (polling, 명령 등록, 스케줄러 시작)
├── handlers.py         # /mbti, /test 핸들러 로직
├── cheer.py            # 아침 응원 메시지 생성·전송
├── scheduler.py        # APScheduler (평일 CHEER_TIME, KST)
├── mbti_logic.py       # MBTI 검증, 요일별 점수, 히어로 선정
├── messages.py         # 응원·등록 확인 메시지 템플릿
├── storage.py          # members.json 읽기/쓰기 (DATA_DIR)
├── telegram_client.py  # Telegram sendMessage API
├── data/members.json   # 팀원 MBTI 저장 (로컬, git 미포함 가능)
├── Procfile            # worker: python app.py
├── railway.toml        # Nixpacks 빌드 설정
├── runtime.txt         # Python 3.11
├── requirements.txt
└── .env.example
```

## 로컬 실행

Python 3.11+ 필요.

```bash
cd CheerBot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID 설정
python app.py
```

그룹 채팅에서 `/mbti ENFP` 등으로 등록한 뒤, `/test`로 미리보기를 확인하거나 설정한 시간에 응원 메시지가 전송됩니다.

> **주의:** 같은 봇 토큰으로 polling을 두 곳에서 동시에 실행하면 Telegram 업데이트가 충돌합니다(409). Railway에 배포한 뒤에는 Railway 인스턴스만 실행하세요.

### 사전 준비

1. [@BotFather](https://t.me/BotFather)에서 `/newbot`으로 봇 생성 → **Bot Token** 복사
2. 팀 그룹에 봇 초대 후 `/chatid`로 그룹 ID 확인 (보통 `-100xxxxxxxxxx` 형태)

## Railway 배포

이 프로젝트는 **Railway**에서 `python app.py` polling + APScheduler로 상시 실행됩니다.

### 1. GitHub 연결

1. [railway.app](https://railway.app) 로그인
2. **New Project** → **Deploy from GitHub repo**
3. 저장소 **SeeYounsunny/CheerBot** 선택, 브랜치 **main**

### 2. 환경 변수

서비스 → **Variables** 탭에서 설정 (아래 [환경 변수](#환경-변수) 참고).

### 3. 서비스 유형 (Worker)

이 봇은 HTTP API 서버가 아니라 Telegram **long polling** 프로세스입니다.

- **권장:** Railway 서비스 유형을 **Worker**로 설정합니다. `Procfile`의 `worker: python app.py`가 사용됩니다.
- Web 서비스로 배포된 경우: `PORT`가 설정되면 `app.py`가 `GET /` → `ok` 헬스 체크를 열어 배포가 통과하도록 합니다.

`railway.toml`에 `startCommand`를 두지 않습니다. Procfile의 `worker:` 설정을 덮어쓰면 Web 전용으로 뜨며 재시작 루프가 날 수 있습니다.

### 4. Volume (데이터 영속화)

Railway 컨테이너 디스크는 **휘발성**입니다. 재배포 후에도 `/mbti` 등록을 유지하려면 Volume을 붙입니다.

1. Railway 프로젝트 → **CheerBot 서비스** → **Volumes** → **Add Volume**
2. **Mount Path:** `/app/data` (Nixpacks 배포 시 앱 루트 `/app`, 기본 `DATA_DIR=data`와 일치)
3. **Redeploy** 후 로그에서 `Member storage: ... at /app/data/members.json` 확인
4. `/mbti` 등록 → 재배포 → 등록 수(`N`)가 유지되는지 확인

> **경고:** Volume 없이 재배포하면 등록한 팀원 목록이 **전부 초기화**됩니다.

Mount Path를 다르게 썼다면 Variables에 `DATA_DIR`을 맞춰 설정하세요. (예: Mount Path `/data` → `DATA_DIR=/data`)

### 5. 배포 확인

1. **Deployments** → **View Logs**
2. 정상 로그 예: `CheerBot starting`, `Webhook cleared; polling mode active`, `Starting MBTI cheer bot (polling mode)...`
3. Telegram 그룹에서 `/mbti ENFP`, `/test` 테스트

## 환경 변수

| 변수 | 필수 | 설명 | 예시 |
|------|------|------|------|
| `TELEGRAM_BOT_TOKEN` | ✅ | BotFather에서 발급한 봇 토큰 | `123456:ABC...` |
| `TELEGRAM_CHAT_ID` | ✅ | 아침 응원을 받을 그룹 채팅 ID | `-1001234567890` |
| `CHEER_TIME` | | 평일 응원 시각 (KST, HH:MM) | `09:00` (기본값) |
| `DATA_DIR` | | `members.json` 저장 폴더 | `data` (기본값, Railway Volume은 `/app/data`) |

로컬에서는 `.env.example`을 복사해 `.env`에 설정합니다. **`.env`는 커밋하지 마세요.**

## 트러블슈팅

| 증상 | 조치 |
|------|------|
| `Missing required environment variable: TELEGRAM_BOT_TOKEN` | Railway Variables에 토큰·채팅 ID 추가 후 재배포 |
| `/mbti` 입력해도 봇이 무반응 | 봇 프로세스 실행 여부, 단톡방 초대·메시지 권한, 슬래시(`/`) 명령 형식 확인 |
| `Conflict: terminated by other getUpdates` (409) | 같은 토큰으로 로컬 + Railway 동시 polling — 한쪽만 실행 |
| 아침 응원이 안 옴 | 주말 여부, 최소 1명 `/mbti` 등록, `TELEGRAM_CHAT_ID`가 대상 그룹과 일치하는지 확인 (`/chatid`) |
| 재배포 후 MBTI 등록이 사라짐 | Railway Volume을 `/app/data`에 마운트했는지 확인 |
| `Invalid CHEER_TIME` | `HH:MM` 형식 사용 (예: `09:00`) |
| `Application failed to respond` | Worker로 전환하거나 최신 `app.py`(PORT 헬스 서버)로 재배포 |

## 데이터

팀원 MBTI는 별도 DB 없이 `{DATA_DIR}/members.json` (기본 `data/members.json`)에 저장됩니다. Telegram user ID를 키로 사용하며, 재등록 시 덮어씁니다. 저장 시 임시 파일에 쓴 뒤 rename하여 손상을 줄입니다.

시작 로그: `Member storage: N registered member(s) at ...` — Railway에서 `N`이 0이면 Volume 미연결 또는 경로 불일치를 의심하세요.
