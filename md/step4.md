# 목표
- 랭체인 이해, 간단한 체인 구성, llm 호출
- 체인구성
  - 프롬프트 구성 -> llm 호출
  - 해당 구성은 향후 복잡한 agent 구성으로 확장

# 구조
```
/
L app
  L llm.py : LLM 모듈
L steps
  L step4_langchain_basic.py  : 체인구성 (prompt | llm)
```

# 실행
```
python -m steps.step4_langchain_basic
---
# LangChain Runnable 파이프라인

## 핵심 개념

LangChain의 **Runnable**은 모든 컴포넌트(프롬프트, LLM, 파서 등)를 동일한 인터페이스로 다루는 표준 규격입니다. `invoke()`, `batch()`, `stream()` 같은 공통 메서드를 제공하며, **LCEL(LangChain Expression Language)**의 `|` 파이프 연산자로 여러 컴포넌트를 체이닝할 수 있습니다.

## 기본 구조

```
프롬프트 | LLM | 출력파서
```

각 단계의 출력이 다음 단계의 입력으로 자동 전달됩니다.

## 예시: 영화 추천 체인

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. 프롬프트 템플릿 정의
prompt = ChatPromptTemplate.from_template(
    "장르: {genre}\n이 장르의 영화 1개를 추천하고 한 줄로 이유를 설명해줘."
)

# 2. LLM 정의
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# 3. 출력 파서 정의
output_parser = StrOutputParser()

# 4. Runnable 파이프라인 구성 (LCEL)
chain = prompt | llm | output_parser

# 5. 실행
result = chain.invoke({"genre": "SF"})
print(result)
```

**출력 예시:**
```
"인터스텔라"를 추천합니다. 시간과 사랑, 물리학을 아름답게 엮어낸 압도적인 영상미 때문입니다.
```

## 동작 흐름

| 단계 | 입력 | 출력 |
|------|------|------|
| prompt | `{"genre": "SF"}` | 완성된 프롬프트 텍스트 |
| llm | 프롬프트 텍스트 | AI 응답 메시지 객체 |
| output_parser | 메시지 객체 | 순수 문자열 |

## 왜 유용한가?

- **일관된 인터페이스**: 모든 컴포넌트가 `invoke`, `stream`, `batch`, `ainvoke`(비동기) 지원
- **가독성**: 복잡한 로직을 파이프로 직관적으로 표현
- **병렬/분기 처리**: `RunnableParallel`, `RunnableBranch`로 확장 가능

```python
result = chain.batch([{"genre": "SF"}, {"genre": "코미디"}])  # 여러 입력 동시 처리
for chunk in chain.stream({"genre": "호러"}):  # 스트리밍 출력
    print(chunk, end="")
```
```