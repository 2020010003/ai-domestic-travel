🧳 AI 국내 여행지 추천 프로그램

입력한 여행 날짜를 바탕으로 AI가 국내 여행지를 추천하고, 여행 정보와 맛집 후보를 생성한 뒤 Markdown 여행 리포트로 정리해주는 Python 프로그램입니다.

핵심 흐름

여행 날짜 입력 → AI 여행지 추천 → 맛집 후보 생성 → 최종 여행 리포트 작성 → JSON + Markdown 저장

📌 1. 프로젝트 한눈에 보기

이 프로그램은 여행 날짜만 입력하면 AI를 활용해 여행 계획에 필요한 정보를 단계적으로 만들어줍니다.

프로그램 실행 흐름

┌──────────────────────┐
│ ① 여행 날짜 입력      │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ ② AI 여행지 추천      │
│  · 여행지             │
│  · 날씨 정보          │
│  · 행사/축제 후보     │
│  · 맛집 후보          │
│  · 추천 이유          │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ ③ AI 최종 리포트 작성 │
│  · 여행 정보 정리      │
│  · 맛집 리스트         │
│  · 1일 여행 일정       │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ ④ 결과 파일 저장      │
│  · JSON               │
│  · Markdown           │
└──────────────────────┘

현재 버전의 특징

기존에는 Kakao Local API를 이용해 맛집을 검색했지만, 현재 버전에서는 Kakao API를 사용하지 않습니다.

따라서 다음 과정이 필요하지 않습니다.

❌ Kakao 회원가입

❌ Kakao REST API 키

❌ 별도의 지도 API

❌ 맛집 검색을 위한 외부 API 호출

대신 첫 번째 AI 요청에서 여행지와 맛집 후보를 함께 생성하도록 프로그램을 단순화했습니다.

✨ 2. 주요 기능

① 여행 날짜 입력

터미널에서 여행 날짜를 입력합니다.

python main.py -date 2025-05-05

입력한 날짜는 YYYY-MM-DD 형식인지 먼저 검사합니다.

② AI에게 여행지 추천받기

입력한 날짜를 AI에게 전달하면 국내 여행지를 추천받습니다.

AI는 다음 정보를 JSON 형식으로 반환합니다.

항목

내용

recommended_city

추천 여행지

weather

해당 시기의 일반적인 날씨

events

행사/축제 후보

reason

여행지 추천 이유

restaurants

맛집 후보

예시:

{
  "recommended_city": "제주도",
  "weather": "5월 초 제주도는 비교적 온화한 날씨가 예상됩니다.",
  "events": [
    "지역 문화 행사 후보"
  ],
  "reason": "5월은 제주를 여행하기 좋은 계절입니다.",
  "restaurants": [
    {
      "name": "맛집 후보 1",
      "address": "제주도 ○○시",
      "category": "제주 향토음식"
    }
  ]
}

⚠️ 맛집 정보에 대한 주의

현재 맛집 정보는 외부 지도 API에서 실시간 검색한 결과가 아니라 AI가 생성한 추천 후보입니다.

따라서 실제 여행 전에 다음 정보를 별도로 확인해야 합니다.

실제 매장 존재 여부

영업 여부

정확한 주소

운영시간

메뉴 및 가격

📝 3. 최종 여행 리포트

첫 번째 AI 응답을 다시 AI에게 전달하여 사람이 읽기 쉬운 Markdown 형식의 최종 여행 리포트를 생성합니다.

리포트에는 다음 내용이 포함됩니다.

# 여행지 이름 여행 추천 리포트

## 1. 추천 지역 및 추천 이유

## 2. 날씨 요약

## 3. 행사/축제 목록

## 4. 맛집 리스트

## 5. 1일 여행 일정
### 오전
### 오후
### 저녁

즉, AI가 만든 여러 정보를 한 번 더 정리하여 실제로 읽고 활용하기 쉬운 여행 계획서로 만드는 구조입니다.

📂 4. 프로젝트 구조

travel/
│
├─ main.py                  # 프로그램 전체 실행 코드
├─ README.md                # 프로젝트 설명서
├─ requirements.txt         # 필요한 Python 패키지
├─ .env                     # API 키 저장
├─ .gitignore               # Git 업로드 제외 파일 설정
│
└─ results/
   ├─ 20250505_raw_data.json
   └─ 20250505_travel_report.md

파일별 역할

파일/폴더

역할

main.py

여행 추천 프로그램의 전체 실행 코드

README.md

프로젝트 설명 및 실행 방법

requirements.txt

필요한 Python 패키지 목록

.env

API 키 저장

.gitignore

API 키 및 불필요한 파일의 Git 업로드 방지

results/

프로그램 실행 결과 저장

⚙️ 5. 설치 및 실행

Step 1. Python 설치 확인

python --version

Python 버전이 출력되면 정상입니다.

Step 2. 필요한 라이브러리 설치

pip install -r requirements.txt

현재 필요한 패키지는 다음과 같습니다.

openai
python-dotenv

Step 3. API 키 설정

프로젝트 폴더의 .env 파일에 코디세이에서 발급받은 API 키를 입력합니다.

OPENAI_API_KEY=발급받은_API_KEY

🔒 .env에는 실제 API 키가 들어가기 때문에 GitHub에 업로드하면 안 됩니다.
.gitignore에 .env가 포함되어 있어 Git 업로드 대상에서 제외됩니다.

Step 4. 프로그램 실행

python main.py -date 2025-05-05

정상적으로 실행되면 다음과 같은 순서로 진행됩니다.

[1단계] AI에게 여행지를 추천받습니다.
[2단계] AI가 추천한 맛집 정보를 확인합니다.
[3단계] AI에게 최종 여행 리포트를 요청합니다.
[4단계] 결과 파일을 저장합니다.

📁 6. 실행 결과

프로그램 실행 후 results 폴더에 두 개의 파일이 저장됩니다.

JSON 원본 데이터

results/20250505_raw_data.json

AI가 생성한 여행 추천 데이터와 오류 정보를 구조화된 JSON 형태로 저장합니다.

Markdown 여행 리포트

results/20250505_travel_report.md

최종 여행 계획을 사람이 읽기 쉬운 Markdown 문서로 저장합니다.

🔄 7. 프로그램 동작 원리

프로그램 전체 흐름은 4단계입니다.

1단계 — 여행지 추천

recommendation = get_first_recommendation(
    date_text,
    errors
)

사용자가 입력한 날짜를 AI에게 전달하고 여행지 추천을 요청합니다.

AI의 응답은 JSON으로 받아 Python dictionary 형태로 처리합니다.

2단계 — 맛집 후보 확인

restaurants = recommendation.get(
    "restaurants",
    []
)

별도의 지도 API를 호출하지 않고 1단계에서 AI가 생성한 맛집 후보를 사용합니다.

3단계 — 최종 리포트 생성

report = generate_final_report(
    recommendation,
    errors
)

1단계에서 얻은 여행 정보를 다시 AI에게 전달하여 Markdown 형식의 최종 여행 리포트를 생성합니다.

4단계 — 결과 저장

json_path, md_path = save_results(
    date_text=date_text,
    recommendation=recommendation,
    report=report,
    errors=errors
)

최종 결과를 다음 두 가지 형태로 저장합니다.

JSON       → 프로그램에서 활용하기 위한 원본 데이터
Markdown   → 사람이 읽기 위한 최종 여행 리포트

🛡️ 8. 오류 처리

프로그램은 일부 오류가 발생하더라도 가능한 경우 전체 실행이 중단되지 않도록 구성되어 있습니다.

처리하는 오류의 예:

AI 첫 번째 응답 처리 실패

AI 응답의 JSON 형식 오류

최종 리포트 생성 실패

오류가 발생하면 errors 리스트에 오류 내용을 저장합니다.

또한 AI 여행지 추천에 실패하는 경우 기본 여행지로 부산을 사용하는 예외 처리가 포함되어 있습니다.

🗺️ 9. 왜 Kakao API를 제거했는가?

기존 버전에서는 Kakao Local API를 사용하여 맛집을 검색했습니다.

하지만 실행 과정에서 다음과 같은 인증 오류가 발생했습니다.

Kakao API 실패: status_code=401
AccessDeniedError

맛집 검색을 위해 별도의 API 키와 인증 설정도 필요했습니다.

기존 구조

AI 여행지 추천
      ↓
Kakao Local API
      ↓
맛집 검색
      ↓
AI 최종 리포트

현재 구조

AI 여행지 + 맛집 후보 생성
      ↓
AI 최종 리포트

프로그램의 핵심 목적이 AI를 활용한 국내 여행지 추천 및 여행 리포트 생성이므로, 별도의 지도 API를 제거하여 프로젝트 구조를 단순화했습니다.

현재 프로그램에서 필요한 외부 API는 코디세이의 OpenAI 호환 API 하나입니다.

⚠️ 10. 데이터 이용 시 주의사항

이 프로그램의 결과는 여행 계획을 위한 추천 자료입니다.

특히 다음 정보는 실시간으로 검증된 정보가 아닐 수 있습니다.

맛집 정보

행사/축제 정보

행사 날짜

날씨

영업시간

주소 및 위치

메뉴 및 가격

따라서 실제 여행 전에 공식 홈페이지나 지도 서비스 등을 통해 최신 정보를 확인하는 것을 권장합니다.

🧰 11. 사용 기술

기술

용도

Python

프로그램 전체 구현

OpenAI Python SDK

AI API 호출

Codyssey OpenAI 호환 API

AI 요청 처리

GPT-5-mini

여행 정보 생성 및 리포트 작성

python-dotenv

.env 환경변수 로드

JSON

AI 응답 및 원본 데이터 저장

Markdown

최종 여행 리포트 저장

🔌 12. API 연결 구조

프로그램은 OpenAI Python SDK를 사용하지만, 실제 요청은 코디세이에서 제공하는 OpenAI 호환 API로 전송합니다.

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://copa.codyssey.kr/v1"
)

전체 연결 구조는 다음과 같습니다.

Python 프로그램
      │
      │ OpenAI Python SDK
      ↓
Codyssey OpenAI 호환 API
      │
      ↓
GPT-5-mini
      │
      ↓
여행 추천 및 여행 리포트 생성

🚀 13. 빠른 시작

# 1. 패키지 설치
pip install -r requirements.txt

# 2. .env 설정
OPENAI_API_KEY=발급받은_API_KEY

# 3. 프로그램 실행
python main.py -date 2025-05-05

실행이 완료되면:

results/
├─ 20250505_raw_data.json
└─ 20250505_travel_report.md

결과 파일이 생성됩니다.

🎯 프로젝트 핵심

여행 날짜 하나를 입력하면 AI가 여행지와 여행 정보를 생성하고, 이를 하나의 여행 리포트로 정리해주는 프로그램입니다.

Kakao API를 제거하고 AI 하나를 중심으로 여행지 추천 → 맛집 후보 생성 → 최종 리포트 작성이 이어지도록 구성하여 외부 API 의존성을 줄였습니다.
