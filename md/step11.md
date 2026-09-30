# 목표
- 랭체인 Tool 구성
- SQL 수행 TOOL, RAG TOOL, ... 외부도구 연결(MCP) (노션, 슬렉, 카톡, 외부s/w, 데탑s/w, 뱅킹)
- 도구 구성하여 에이전트가 자율적으로 판단하여 도구를 사용하도록 구성 => 랭그래프 출현

# 구조
```
/
L app
  L tools
    L __init__.py
    L rag_tools.py    : rag를 도구로 사용할 수 있는 내용 적제 -> @tool
    L sql_tools.py    : sql을 도구로 사용할 수 있는 내용 적제 -> @tool
L steps
  L step11_tools.py   : 툴 사용 테스트 코드
L sql
  L 003_business.sql  : sql 툴을 위한 대상 테이블과 더미 데이터
```

# 테이블 생성 및 데이터 삽입
```
python -m scripts.migrate
```