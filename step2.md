# 목표
- AWS Bedrock를 이용하여 LLM을 직접 호출
```
AWS 인증 > Bedrock Runtime Client 생성 > LLM에게 프롬프트 전달 > 응답 파싱(JSON)
```

# 구조
/
L app/            : 모듈 (타 프로젝트에서도 사용 가능하게 구조화)
  L bedrock.py    : Bedrock Runtime Client 생성
  L config.py     : 프로젝트 전체 환경변수 총괄 관리 (.env 로드, 추가)
L steps/
  L step2_bedrock_llm_call.py : llm 호출 및 응답 처리

# 실행
```
python -m steps.step2_bedrock_llm_call

---

# AI Agent 5줄 설명

1. **정의**: AI Agent는 목표를 달성하기 위해 스스로 판단하고 행동하는 자율적인 AI 시스템입니다.

2. **인식**: 환경(데이터, 사용자 입력, 외부 API 등)으로부터 정보를 수집하고 상황을 인식합니다.

3. **판단**: 수집된 정보를 바탕으로 목표 달성에 필요한 계획을 세우고 다음 행동을 결정합니다.

4. **실행**: 도구 사용, API 호출, 코드 실행 등 실제 행동을 통해 작업을 수행합니다.

5. **반복 개선**: 결과를 관찰하고 피드백을 반영하여 다음 행동을 조정하는 과정을 반복합니다.
```