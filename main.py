import argparse
import json
import os
from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# 1. 환경 변수 로드
# ============================================================

# .env 파일에 적어둔 API 키를 가져옵니다.
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# ============================================================
# 2. 코디세이 API 설정
# ============================================================

# 코디세이에서 제공하는 OpenAI 호환 API 주소입니다.
OPENAI_BASE_URL = "https://copa.codyssey.kr/v1"

# 코디세이 예제에서 사용하는 모델입니다.
MODEL_NAME = "gpt-5-mini"


# ============================================================
# 3. OpenAI 클라이언트 만들기
# ============================================================

# 중요:
# 실제 OpenAI 서버가 아니라
# 코디세이 서버를 사용하도록 base_url을 변경합니다.
#
# 따라서 아래 코드는
#
# "코디세이 API 주소 + 내 API 키"
#
# 로 연결하는 역할을 합니다.

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)


# ============================================================
# 4. 환경 변수 확인
# ============================================================

def validate_env():
    """
    .env 파일에 코디세이/OpenAI API 키가 제대로 들어있는지 확인합니다.
    """

    if not OPENAI_API_KEY:
        print()
        print("[오류] OPENAI_API_KEY가 없습니다.")
        print()
        print(".env 파일에 다음과 같이 입력해주세요:")
        print()
        print("OPENAI_API_KEY=코디세이에서_발급받은_API_KEY")
        print()
        raise SystemExit(1)


# ============================================================
# 5. 날짜 검사
# ============================================================

def validate_date(date_text):
    """
    입력한 날짜가 YYYY-MM-DD 형식인지 확인합니다.
    """

    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True

    except ValueError:
        return False


# ============================================================
# 6. AI 응답에서 텍스트 가져오기
# ============================================================

def extract_llm_text(response):
    """
    코디세이 API에서 받은 응답에서
    AI가 작성한 텍스트를 가져옵니다.
    """

    # 응답이 그냥 문자열인 경우
    if isinstance(response, str):
        return response

    # 응답이 dictionary인 경우
    if isinstance(response, dict):
        try:
            return response["choices"][0]["message"]["content"]

        except Exception:
            return str(response)

    # OpenAI SDK 응답인 경우
    try:
        return response.choices[0].message.content

    except Exception:
        return str(response)


# ============================================================
# 7. AI가 만들어준 JSON 가져오기
# ============================================================

def extract_json_from_text(text):
    """
    AI가 JSON을 만들어줬을 때
    JSON 부분만 찾아서 Python dictionary로 변환합니다.

    예를 들어 AI가

    ```json
    {
        "recommended_city": "부산"
    }
    ```

    이렇게 보내도 처리할 수 있습니다.
    """

    text = text.strip()

    # Markdown 코드블록 제거
    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```JSON", "")
        text = text.replace("```", "")
        text = text.strip()

    # JSON 시작 위치
    start = text.find("{")

    # JSON 끝 위치
    end = text.rfind("}")

    # JSON만 잘라냅니다.
    if start != -1 and end != -1 and start < end:
        text = text[start:end + 1]

    # JSON → Python dictionary
    return json.loads(text)


# ============================================================
# 8. results 폴더 만들기
# ============================================================

def ensure_results_folder():
    """
    결과를 저장할 results 폴더가 없으면 만들어줍니다.
    """

    if not os.path.exists("results"):
        os.makedirs("results")


# ============================================================
# 9. 코디세이 AI 호출
# ============================================================

def call_llm(messages):
    """
    코디세이의 OpenAI 호환 API를 호출합니다.

    여기서 실제로 하는 일은
    코디세이 서버에 AI에게 질문을 보내는 것입니다.
    """

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages
    )

    return extract_llm_text(response)


# ============================================================
# 10. 첫 번째 AI 여행지 추천
# ============================================================

def get_first_recommendation(date_text, errors):
    """
    사용자가 입력한 날짜를 바탕으로
    AI에게 국내 여행지를 추천받습니다.
    """

    prompt = f"""
너는 국내 여행 추천 전문가야.

사용자가 입력한 여행 날짜는 "{date_text}"야.

아래 JSON 형식만 사용해서 답변해.

중요:
- 설명 문장을 JSON 바깥에 작성하지 마.
- Markdown을 사용하지 마.
- 반드시 JSON 하나만 출력해.

필수 JSON 형식:

{{
  "recommended_city": "string",
  "weather": "string",
  "events": ["string", "string"],
  "reason": "string",
  "restaurants": [
    {{
      "name": "string",
      "address": "string",
      "category": "string"
    }}
  ]
}}

조건:

1. recommended_city
   - 대한민국의 여행지 또는 도시를 추천해.

2. weather
   - 해당 날짜의 계절을 고려한 일반적인 날씨를 설명해.
   - 실제 실시간 날씨라고 단정하지 마.

3. events
   - 해당 시기에 여행자가 관심을 가질 만한 행사나 축제 후보를 작성해.
   - 1~3개 정도 작성해.

4. reason
   - 왜 이 여행지를 추천하는지 2~4문장으로 설명해.

5. restaurants
   - 추천 여행지에서 방문해볼 만한 맛집 후보를 3~5개 작성해.
   - 각 맛집에는 name, address, category를 포함해.
   - 실시간 검색 결과가 아니므로 실제 영업 여부나 최신 정보라고 단정하지 마.
"""

    messages = [
        {
            "role": "system",
            "content": (
                "너는 한국 국내 여행 추천 전문가다. "
                "사용자의 날짜를 바탕으로 여행지를 추천하고 "
                "반드시 JSON만 출력한다."
            )
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    try:

        print("AI에게 여행지를 물어보는 중입니다...")

        text = call_llm(messages)

        data = extract_json_from_text(text)

        validate_recommendation_json(data)

        return data

    except Exception as e:

        errors.append(f"1차 AI 추천 실패: {e}")

        print()
        print("[경고] 첫 번째 AI 응답을 처리하지 못했습니다.")
        print("AI에게 한 번 더 질문합니다.")
        print()

        # -------------------------------
        # AI에게 한 번 더 질문
        # -------------------------------

        retry_prompt = f"""
날짜는 {date_text}입니다.

반드시 아래 JSON만 출력하세요.

{{
  "recommended_city": "부산",
  "weather": "해당 계절의 일반적인 날씨",
  "events": ["행사 후보 1", "행사 후보 2"],
  "reason": "추천 이유를 2~4문장으로 작성",
  "restaurants": [
    {{
      "name": "맛집 후보 1",
      "address": "주소 정보",
      "category": "음식 종류"
    }},
    {{
      "name": "맛집 후보 2",
      "address": "주소 정보",
      "category": "음식 종류"
    }}
  ]
}}
"""

        retry_messages = [
            {
                "role": "system",
                "content": "반드시 JSON만 출력하는 여행 추천 AI입니다."
            },
            {
                "role": "user",
                "content": retry_prompt
            }
        ]

        try:

            text = call_llm(retry_messages)

            data = extract_json_from_text(text)

            validate_recommendation_json(data)

            return data

        except Exception as retry_error:

            errors.append(
                f"AI 추천 재시도 실패: {retry_error}"
            )

            print()
            print("[경고] AI 추천을 받지 못했습니다.")
            print("기본 여행지 부산을 사용합니다.")
            print()

            # AI가 완전히 실패했을 경우 사용할 기본값
            return {
                "recommended_city": "부산",
                "weather": (
                    "해당 계절의 일반적인 날씨를 참고해 "
                    "여행 준비를 하는 것이 좋습니다."
                ),
                "events": [
                    "지역 축제 또는 문화 행사 확인 필요"
                ],
                "reason": (
                    "AI 추천에 실패하여 기본 여행지로 부산을 "
                    "선택했습니다. 부산은 바다와 관광지가 많아 "
                    "국내 여행지로 활용하기 좋은 지역입니다."
                ),
                "restaurants": []
            }


# ============================================================
# 11. AI 추천 JSON 검사
# ============================================================

def validate_recommendation_json(data):
    """
    AI가 만든 JSON에 필요한 항목이 모두 있는지 확인합니다.
    """

    required_keys = [
        "recommended_city",
        "weather",
        "events",
        "reason",
        "restaurants"
    ]

    for key in required_keys:

        if key not in data:
            raise ValueError(
                f"필수 항목이 없습니다: {key}"
            )

    if not isinstance(
        data["recommended_city"],
        str
    ):
        raise TypeError(
            "recommended_city는 문자열이어야 합니다."
        )

    if not isinstance(
        data["weather"],
        str
    ):
        raise TypeError(
            "weather는 문자열이어야 합니다."
        )

    if not isinstance(
        data["events"],
        list
    ):
        raise TypeError(
            "events는 리스트여야 합니다."
        )

    if not isinstance(
        data["reason"],
        str
    ):
        raise TypeError(
            "reason은 문자열이어야 합니다."
        )

    if not isinstance(
        data["restaurants"],
        list
    ):
        raise TypeError(
            "restaurants는 리스트여야 합니다."
        )

    for restaurant in data["restaurants"]:
        if not isinstance(restaurant, dict):
            raise TypeError(
                "restaurants의 각 항목은 dictionary여야 합니다."
            )

        for key in ["name", "address", "category"]:
            if key not in restaurant:
                raise ValueError(
                    f"맛집 정보에 필수 항목이 없습니다: {key}"
                )


# ============================================================
# 12. 최종 여행 리포트 만들기
# ============================================================

def generate_final_report(
    recommendation,
    errors
):
    """
    첫 번째 AI 추천 결과를 바탕으로
    최종 여행 리포트를 만듭니다.
    """

    recommendation_text = json.dumps(
        recommendation,
        ensure_ascii=False,
        indent=2
    )

    prompt = f"""
너는 국내 여행 플래너야.

아래 데이터를 이용해서
한국어 Markdown 여행 리포트를 작성해줘.

[AI 여행지 추천 정보]

{recommendation_text}


[AI가 추천한 맛집 후보]

추천 데이터의 restaurants 항목을 사용합니다.
실시간 검색 결과가 아니므로 실제 영업 여부나 최신 정보라고 단정하지 마세요.


리포트에는 반드시 아래 내용을 포함해.

# 여행지 이름 여행 추천 리포트

## 1. 추천 지역 및 추천 이유

추천 지역과 추천 이유를 설명해.

## 2. 날씨 요약

제공된 날씨 정보를 정리해.

## 3. 행사/축제 목록

행사를 목록으로 보여줘.

## 4. 맛집 리스트

맛집 이름, 주소, 카테고리를 보여줘.

맛집이 없다면:

데이터 없음

이라고 작성해.

## 5. 1일 여행 일정

### 오전

어디를 방문하면 좋은지 작성해.

### 오후

어디를 방문하면 좋은지 작성해.

### 저녁

맛집과 저녁 일정을 작성해.

주의:

- 실제 확인되지 않은 정보를 확정적인 사실처럼 표현하지 마.
- 보기 쉽게 Markdown으로 작성해.
- 친절한 한국어로 작성해.
"""

    messages = [
        {
            "role": "system",
            "content": (
                "너는 한국어 Markdown 여행 리포트를 "
                "작성하는 여행 플래너다."
            )
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    try:

        print("AI에게 최종 여행 리포트를 작성하도록 요청합니다...")

        report = call_llm(messages)

        return report

    except Exception as e:

        errors.append(
            f"최종 리포트 생성 실패: {e}"
        )

        print()
        print("[경고] 최종 AI 리포트 생성에 실패했습니다.")
        print("기본 리포트를 만듭니다.")
        print()

        city = recommendation.get(
            "recommended_city",
            "추천 여행지"
        )

        weather = recommendation.get(
            "weather",
            "정보 없음"
        )

        events = recommendation.get(
            "events",
            []
        )

        reason = recommendation.get(
            "reason",
            "정보 없음"
        )

        lines = []

        lines.append(
            f"# {city} 여행 추천 리포트"
        )

        lines.append("")

        lines.append(
            "## 1. 추천 지역 및 추천 이유"
        )

        lines.append(reason)

        lines.append("")

        lines.append(
            "## 2. 날씨 요약"
        )

        lines.append(weather)

        lines.append("")

        lines.append(
            "## 3. 행사/축제 목록"
        )

        if events:

            for event in events:
                lines.append(
                    f"- {event}"
                )

        else:

            lines.append(
                "- 데이터 없음"
            )

        lines.append("")

        lines.append(
            "## 4. 맛집 리스트"
        )

        restaurants = recommendation.get(
            "restaurants",
            []
        )

        if restaurants:

            for restaurant in restaurants:

                lines.append(
                    f"- **{restaurant.get('name', '이름 없음')}**"
                )

                lines.append(
                    f"  - 주소: "
                    f"{restaurant.get('address', '주소 없음')}"
                )

                lines.append(
                    f"  - 카테고리: "
                    f"{restaurant.get('category', '정보 없음')}"
                )

        else:

            lines.append(
                "데이터 없음"
            )

        lines.append("")

        lines.append(
            "## 5. 1일 일정 제안"
        )

        lines.append(
            "- 오전: 대표 관광지 방문"
        )

        lines.append(
            "- 오후: 지역 산책 및 카페 방문"
        )

        lines.append(
            "- 저녁: 맛집 방문 후 야경 감상"
        )

        return "\n".join(lines)


# ============================================================
# 14. 결과 파일 저장
# ============================================================

def save_results(
    date_text,
    recommendation,
    report,
    errors
):
    """
    프로그램 결과를 results 폴더에 저장합니다.

    JSON:
    AI 원본 데이터 + AI 추천 맛집 + 오류 정보

    Markdown:
    사람이 읽기 쉬운 여행 리포트
    """

    ensure_results_folder()

    # 예:
    # 2025-05-05
    # ↓
    # 20250505

    safe_date = date_text.replace(
        "-",
        ""
    )

    json_path = (
        f"results/"
        f"{safe_date}_raw_data.json"
    )

    md_path = (
        f"results/"
        f"{safe_date}_travel_report.md"
    )

    raw_data = {
        "input_date": date_text,

        "recommendation": recommendation,

        "errors": errors
    }

    # JSON 파일 저장
    with open(
        json_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            raw_data,
            f,
            ensure_ascii=False,
            indent=2
        )

    # Markdown 파일 저장
    with open(
        md_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(report)

    return json_path, md_path


# ============================================================
# 15. 메인 프로그램
# ============================================================

def main():

    # --------------------------------------------------------
    # 명령어 입력 준비
    # --------------------------------------------------------

    parser = argparse.ArgumentParser(
        description=(
            "AI 국내 여행지 추천 프로그램"
        )
    )

    parser.add_argument(
        "-date",
        "--date",
        required=True,
        help=(
            '여행 날짜를 입력하세요. '
            '예: 2025-05-05'
        )
    )

    args = parser.parse_args()

    date_text = args.date

    # --------------------------------------------------------
    # 날짜 확인
    # --------------------------------------------------------

    if not validate_date(date_text):

        print()
        print(
            "[오류] 날짜 형식이 올바르지 않습니다."
        )

        print()

        print(
            "올바른 형식:"
        )

        print(
            "YYYY-MM-DD"
        )

        print()

        print(
            "예시:"
        )

        print(
            "python main.py -date 2025-05-05"
        )

        raise SystemExit(1)

    # --------------------------------------------------------
    # API 키 확인
    # --------------------------------------------------------

    validate_env()

    # 오류를 모아둘 리스트
    errors = []

    # --------------------------------------------------------
    # 프로그램 시작
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("      AI 국내 여행지 추천 프로그램")
    print("=" * 60)

    print()

    print(
        f"입력한 여행 날짜: {date_text}"
    )

    print()

    # --------------------------------------------------------
    # 1단계
    # --------------------------------------------------------

    print(
        "[1단계] AI에게 여행지를 추천받습니다."
    )

    recommendation = get_first_recommendation(
        date_text,
        errors
    )

    city = recommendation.get(
        "recommended_city",
        "부산"
    )

    print()

    print(
        f"AI 추천 여행지: {city}"
    )

    print()

    # --------------------------------------------------------
    # 2단계
    # --------------------------------------------------------

    print(
        "[2단계] AI가 추천한 맛집 정보를 확인합니다."
    )

    restaurants = recommendation.get(
        "restaurants",
        []
    )

    print(
        f"추천된 맛집 후보 수: {len(restaurants)}개"
    )

    print()

    # --------------------------------------------------------
    # 3단계
    # --------------------------------------------------------

    print(
        "[3단계] AI에게 최종 여행 리포트를 요청합니다."
    )

    report = generate_final_report(
        recommendation,
        errors
    )

    print()

    # --------------------------------------------------------
    # 4단계
    # --------------------------------------------------------

    print(
        "[4단계] 결과 파일을 저장합니다."
    )

    json_path, md_path = save_results(
        date_text=date_text,
        recommendation=recommendation,
        report=report,
        errors=errors
    )

    # --------------------------------------------------------
    # 완료
    # --------------------------------------------------------

    print()

    print("=" * 60)
    print("                실행 완료")
    print("=" * 60)

    print()

    print(
        f"원본 JSON 저장 위치: {json_path}"
    )

    print(
        f"최종 리포트 저장 위치: {md_path}"
    )

    # --------------------------------------------------------
    # 오류가 있었다면 보여주기
    # --------------------------------------------------------

    if errors:

        print()

        print(
            "[주의] 실행 중 일부 문제가 발생했습니다."
        )

        for error in errors:

            print(
                f"- {error}"
            )

    print()


# ============================================================
# 16. 프로그램 시작
# ============================================================

if __name__ == "__main__":
    main()
