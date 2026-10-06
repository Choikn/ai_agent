# 목표
- 하네스 엔지니어링 
    - 바이브 코딩
        - 코딩 에이전트가 코드를 안전하고, 일관되게, 불필요한 작업 x, 항상 기억할 내용 세팅등 반영하여
        - 코드 작성,실행,검증하도록 전체를 둘러싸고 있는 실행 환경, 규칙 전체를 의미
        - ex) claude.md
    - Agent의 Tool 실행
        - Agent가 동작할 수 있는 범위, 권한, 비용, 시간, 검증 규칙등 설계하는 것

# 비교
| 개념 | Coding Agent Harness | 현재 Agent Harness |
|---|---|---|
| 실행 대상 | 코드·Shell·파일·Git | Tool |
| 권한 통제 | 허용 명령/경로 | `ALLOWED_TOOLS` |
| 실행 제한 | timeout, 최대 반복 | `Budget` |
| 위험 작업 차단 | rm, 임의 shell 등 | `assert_allowed_tool()` |
| 검증 | test/lint/build | Tool 결과/Verifier |
| 목적 | 코딩 Agent 통제 | 업무 Agent 통제 |

# 구성
```
/
L app
    L harness.py    : 정책 계층 구성
    L agent
        L graph.py  : 하네스 노드 반영 -> 제한 정책을 에이전트 반영
L steps
    L step20_harness_guardrail.py : 하네스를 적용한 에이전트 수행 테스트
```

# 에이전트 구성상 하네스 반영
'''
    Agent
    ↓
    Tool 호출 결정
    ↓
    Harness             ← 실제 개입
    ├─ Tool 권한 검사
    └─ Tool 횟수 검사
    ↓
    ToolNode
    ↓
    Agent
'''

# 실행
```
python -m steps.step20_harness_guardrail
---
하네스 체크 통과 (툴 실행 횟수, 툴 수행시간) 7.200000254670158e-06
consume_tool_round 호출, 라운드 증가 1
하네스 체크 통과 (툴 실행 횟수, 툴 수행시간) 2.510060799999337
하네스 체크 통과 (툴 실행 횟수, 툴 수행시간) 7.599999662488699e-06
++++++++++++++++++++++++++++++
[최종답변]

 {
  "answer": "2026년 9월 매출 요약 (2026-09-01 ~ 2026-09-30)\n- 결제 완료 매출: 3,586,000원\n- 주문 건수: 8건\n- 평균 주문 단가: 약 448,250원\n\n위 수치는 해당 기간 내 결제 완료된 주문만을 집계한 결과입니다.",
  "sources": [
    "sales_summary 도구 조회 결과"
  ],
  "tools_used": [
    "sales_summary"
  ],
  "confidence": 0.8
}
++++++++++++++++++++++++++++++
```