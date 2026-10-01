# 목표
- Agent Memory
- PostgreSQL + pgvector 방식으로 지식 저장(현재) + Memory 저장소 활용
- Memory 저장소 활용하면 짧은 답변, 기존 질문에 대한 답변을 메모리에서 체크하여 LLM 사용 없이 응답 가능한 구조 구성 -> 중요도 관리 -> 토큰 비용(운영비) 절감 도움
- 장기기억 활용

- 역할
  - llm : 판단, 답변을 담당 두뇌
  - RAG : 회사 문서, 규정등 llm 모르는 정보
  - db  : 실제 데이터들 저장, 조회
  - MEMORY : 사용자의 맥락 기억, 패턴 기억 -> 사용자 주의, 답변 형태, 업무 형태, 기억포인트 등등 저장 -> 사용자 질문시 해당 내용을 기반으로 답변할 때 제공
    - 사용자의 선호하는 방식으로 답변을 구성하게 도움
    - llm이 추론을 할 때, 사용자가 누구고, 어떤 업무를 하고, 어떤 방식으로 답변 받기를 원하지는 삽입(프롬프트)
    - llm이 사용자를 처음 만난 사람처럼 행동하지 말고, 과거의 중요한 정보(맥락)을 제공하는 역할 담당

# 구조
```
/
L sql
  L 005_memory.sql    : 사용자의 정보를 저장하는 테이블, 검색
L app
  L tools
    L memory_tools.py : sql 역할 담당, 기능적으로 메모리 역할
  L agent
    L graph.py        : 툴 등록
  L config.py         : 사용자 아이디 환경변수 구성
L steps
  L step14_memory.py  : 메모리 테스트
L .env                : 사용자 아이디 더미 구성(한명을 위한 아이디, 실제론 제거)
```

# sql 반영
```
python -m scripts.migrate
---
\dt

# 테이블 구조 확인
\d agent_memories
```

# 실행
```
python -m steps.step14_memory
---
[최종답변]

 **조회 결과**

현재 저장된 사용자 선호 방식은 다음과 같습니다:

- **답변 형식**: 짧은 bullet(글머리 기호) 형태 선호
- **중요도**: 0.8 (높음)

앞으로 답변 시 이 형식을 기본으로 적용하겠습니다. 혹시 추가로 선호하는 방식(예: 숫자 데이터 우선 제시, 결론 먼저 등)이 있다면 말씀해주시면 함께 기억해두겠습니다.
++++++++++++++++++++++++++++++

--- 
select count(*) from agent_memories;
 count 
-------
     1
(1 row)

agentlab=# select id, left(content, 20) from agent_memories;
 id |              left              
----+--------------------------------
  2 | 답변은 짧은 bullet(글머리 기호
(1 row)
```