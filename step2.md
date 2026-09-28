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