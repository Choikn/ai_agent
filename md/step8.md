# 목표
- 문서 레벨로 디비에 데이터 삽입
- 문서(말뭉치) -> 쪼개는 과정 필요함(청킹, chunk 단위 자름)
    - [v]단순 크기 -> .... -> 시멘틱 청킹(주제가 변경되면 자름)
    - RAG 서비스 => 질문의 포인트는 청킹 기준을 어떻게 수행하였는가?
    - 문서 테이블(1) -> 청킹 테이블(n)
    - 문서 (md + 테스트형태 제공)
        - Markdown fomatter 처리(메터데이터), document chunking 처리 (임베딩처리) 

# 데이터
- cs, sales, hr 관련 사내 규정 문서
- 현재 = 메타 데이터 + 규정 
- 향후 규정 내용을 더 확대 예정 (청킹이 n개로 확장되는것 확인)

# 구조
```
/
L sql 
    L migrations
        L 002_documents.sql
L steps
    L step8_document_ingestion.py
L app
    L ingestion
        L __init__.py
        L ingest.py
        L loader.py
        L splitter.py
```

# 데이터를 백터화 디비 입력 절차
- 002_documents.sql


- 테이블 생성
```
python -m scripts.migrate
```

# 실행
```
python -m steps.step8_document_ingestion
---
select * from documents;
---
 id | document_code  | department | category |         title          |          source          | version | effective_date |          created_at           
----+----------------+------------+----------+------------------------+--------------------------+---------+----------------+-------------------------------
  1 | CS-REFUND-2026 | CS         | refund   | 고객 반품 및 환불 정책 | data\cs\refund_policy.md | 2026.3  | 2026-04-01     | 2026-09-29 05:17:34.311089+00

# 실행결과 확인
--- 
select 
    id, document_id, chunk_index, 
    left(content, 10) || '...' as content,
    left(embedding::text, 10) || '...' as embedding,
    metadata
from 
    document_chunks
order by id;
---
 id | document_id | chunk_index |        content        |        embedding        |                                       metadata                                       
----+-------------+-------------+-----------------------+-------------------------+--------------------------------------------------------------------------------------
  3 |           1 |           0 | # 고객 반품 및 ...    | [-0.11128634,0.02507... | {"category": "refund", "department": "CS", "section_source": "refund_policy.md"}
  4 |           1 |           1 | 환불은 반품 상품이... | [-0.110569924,0.0034... | {"category": "refund", "department": "CS", "section_source": "refund_policy.md"}
  5 |           3 |           0 | # 연차휴가 운영 ...   | [-0.05440052,0.07231... | {"category": "leave", "department": "HR", "section_source": "leave_policy.md"}
  6 |           3 |           1 | 동일 팀에서 여러 ...  | [-0.027998118,0.0521... | {"category": "leave", "department": "HR", "section_source": "leave_policy.md"}
  7 |           4 |           0 | # 국내 출장비 규...   | [0.006254842,0.04359... | {"category": "travel", "department": "HR", "section_source": "travel_policy.md"}
  8 |           4 |           1 | 식비는 별도 영수증... | [-0.02748282,0.04701... | {"category": "travel", "department": "HR", "section_source": "travel_policy.md"}
  9 |           5 |           0 | # 기업 고객 할인...   | [0.013105711,0.05505... | {"category": "discount", "department": "SALES", "section_source": "sales_policy.md"}
 10 |           5 |           1 | 프로모션 할인과 기... | [-0.01832597,0.03932... | {"category": "discount", "department": "SALES", "section_source": "sales_policy.md"}
(8 rows)
```

# 청킹 종류
| 방식 | 기준 | 특징 | 적합한 경우 |
|---|---|---|---|
| **Fixed-size** | 글자/토큰 수 | 가장 단순 | 기본 실습(step8번 적용) |
| **Recursive** | 문단 → 문장 → 글자 | 구조를 최대한 유지 | 일반 RAG ⭐ |
| **Sentence** | 문장 | 문장 단위 보존 | FAQ, 짧은 문서 |
| **Structure-based** | 제목/섹션/Markdown | 문서 구조 보존 | 사내 업무 문서 ⭐ |
| **Semantic** | 의미 유사도 | 의미가 바뀌는 지점에서 분리 | 고급 RAG ⭐ |
| **Parent-Child** | 큰 Chunk + 작은 Chunk | 검색과 답변 컨텍스트 분리 | 긴 문서 |
| **Agentic** | LLM/Agent 판단 | 문맥·주제에 따라 동적 분할 | 고급/Agentic RAG |