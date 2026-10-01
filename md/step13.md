# 목표
- 랭그래프 + 전형데이터(postgresql) + 비정형 데이터(pgvector) 같이 추론의 지식(배경)으로 사용
- 환불 통계(SQL tool)와 환불 정책(Rag tool)을 한 질문에서 함께 처리/사용

# sql
- 환불 통계를 위한 sql 처리
```
python -m scripts.migrate
---
select * from refunds;
 refund_id | order_id |      requested_at      |     reason     |  amount  |  status  
-----------+----------+------------------------+----------------+----------+----------
         1 |        8 | 2026-09-04 09:00:00+00 | product_defect | 99000.00 | approved
(1 row)
```

# 구조
```
/
L steps
  L step13_sql_rag_agent.py : 질문을 가지고 llm 추론 진행
```