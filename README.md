🧳 AI 국내 여행지 추천 프로그램

입력한 여행 날짜를 바탕으로 AI가 여행지, 날씨, 축제, 맛집을 추천하고 일주일/1일 일정 리포트(Markdown & JSON)를 자동으로 작성해 주는 Python CLI 프로그램입니다.

📌 주요 특징 (Key Features)

원스톱 AI 추천: 외부 지도/지역 API(Kakao API 등) 연결 없이, OpenAI 호환 API 단 하나로 여행지 추천부터 맛집 후보, 일정 작성까지 처리합니다.

예외 처리 & Fallback: AI 응답 실패나 JSON 파싱 에러 시에도 기본 데이터(부산 추천)를 활용해 프로그램이 중단되지 않고 완주합니다.

이중 결과 저장: 파이프라인 연동용 JSON 원본과 가독성 높은 Markdown 리포트를 동시에 자동 생성합니다.

🔄 프로그램 흐름 (Workflow)

[① 날짜 입력] ──> [② AI 여행지/맛집 추천] ──> [③ AI 최종 리포트 생성] ──> [④ 파일 저장]
 (CLI Argument)     (JSON 포맷 파싱)           (Markdown 문서 양식)     (results/ 폴더)


여행 날짜 입력: CLI 인자로 날짜(YYYY-MM-DD)를 전달받고 검증합니다.

여행지 및 맛집 추천: 날씨, 추천 이유, 행사/축제, 맛집 후보 정보를 구조화된 JSON 형태로 생성합니다.

최종 리포트 작성: 추천 데이터를 기반으로 사람이 읽기 좋은 양식의 Markdown 여행 보고서를 생성합니다.

결과 자동 저장: results/ 경로에 원본 JSON 데이터와 리포트 Markdown 문서를 저장합니다.

📁 프로젝트 구조 (Project Structure)

travel/
├── main.py                # 전체 실행 프로세스 제어 코드
├── README.md              # 프로젝트 안내 문서
├── requirements.txt       # 의존성 라이브러리 목록
├── .env                   # API Key 등 환경변수 설정 파일
├── .gitignore             # Git 추적 제외 설정
└── results/               # 프로그램 실행 결과 저장 폴더
    ├── YYYYMMDD_raw_data.json
    └── YYYYMMDD_travel_report.md


🛠️ 기술 스택 (Tech Stack)

구분

기술 / 라이브러리

용도

Language

Python 3.x

프로그램 핵심 로직 구현

AI Client

OpenAI Python SDK

API 호출 인터페이스

AI Infrastructure

Codyssey OpenAI Compatible API

LLM 프로바이더 (https://copa.codyssey.kr/v1)

Model

GPT-5-mini

여행지 추천 및 Markdown 리포트 작성을 담당

Env Management

python-dotenv

.env 파일 내 보안 환경변수 로드

⚙️ 설치 및 실행 (Quick Start)

1. 필요한 패키지 설치

pip install -r requirements.txt


2. 환경변수 설정

프로젝트 루트 경로에 .env 파일을 생성하고 발급받은 API Key를 입력합니다.

OPENAI_API_KEY=your_api_key_here


⚠️ 보안 주의: .env 파일에는 실제 API 키가 포함되므로 GitHub 등 public 저장소에 절대 업로드하지 마세요. (.gitignore 등록 완료)

3. 프로그램 실행

-date 인자와 함께 실행하고자 하는 날짜(YYYY-MM-DD)를 입력합니다.

python main.py -date 2025-05-05


📄 실행 결과물 예시

실행이 성공적으로 끝나면 results/ 디렉터리에 파일 두 개가 생성됩니다.

1. Markdown 리포트 (results/20250505_travel_report.md)

# 제주도 여행 추천 리포트

## 1. 추천 지역 및 추천 이유
5월 초 제주도는 따뜻한 봄 날씨와 함께 차귀도, 성산일출봉 등 자연경관을 즐기기 가장 좋은 시기입니다.

## 2. 날씨 요약
낮 기온 18~22도로 비교적 온화하고 야외 활동에 적합합니다.

## 3. 행사/축제 목록
- 제주 봄꽃 축제 및 지역 문화 행사

## 4. 맛집 리스트
- **맛집 A**: 제주 향토음식 전문점
- **맛집 B**: 흑돼지 구이 전문점

## 5. 1일 여행 일정
- **오전**: 성산일출봉 산책 및 해안가 드라이브
- **오후**: 점심 식사 후 제주 문화 행사 참여
- **저녁**: 현지 맛집 방문 및 야시장 구경


2. JSON 원본 데이터 (results/20250505_raw_data.json)

{
  "recommended_city": "제주도",
  "weather": "5월 초 제주도는 비교적 온화한 날씨가 예상됩니다.",
  "events": ["지역 문화 행사 후보"],
  "reason": "5월은 제주를 여행하기 좋은 계절입니다.",
  "restaurants": [
    {
      "name": "맛집 후보 1",
      "address": "제주도 ○○시",
      "category": "제주 향토음식"
    }
  ]
}


⚠️ 주의사항 (Notice)

本 프로그램에서 추천하는 맛집, 행사 일정, 운영시간, 주소 등은 LLM이 생성한 데이터입니다.

실제 방문 전 지도 서비스(네이버 지도, 카카오맵 등)나 공식 홈페이지를 통해 매장 영업 여부 및 최신 정보를 반드시 확인하시기 바랍니다.
