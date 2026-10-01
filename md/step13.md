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
L app
  L agent
    L graph.py              : refund_summary 도구 추가
  L tools
    L sql_tools.py          : 추가로 특정 날짜내에 환불 요청 건수, 금액, 사유등 조회
L steps
  L step13_sql_rag_agent.py : 질문을 가지고 llm 추론 진행
```

# 실행
```
python -m steps.step13_sql_rag_agent
---
=> 도구가 현재 제공되어 있지 않습니다. 특정 미션 해결 x

[최종답변]

 ## 1. 2026-09-01 ~ 2026-09-05 환불 현황 조회 결과

죄송하지만, 현재 제공된 도구 범위 내에서는 **환불(Refund) 데이터를 직접 조회할 수 있는 SQL Tool이 없습니다.**

- `sales_summary` : 결제 **완료** 매출/주문 건수만 집계 (환불 반영 없음)
- `top_products` : 결제 **완료** 매출 기준 상위 제품 (환불 반영 없음)

위 두 도구 모두 "결제 완료" 기준이라 환불·반품 건수나 환불 금액을 산출할 수 있는 데이터 소스가 아닙니다. 따라서 요청하신 기간의 **환불 현황 수치는 확인이 불가능**하며, 임의로 추정하거나 생성하지 않았습니다.

> 필요하시면 해당 기간의 결제 완료 매출(`sales_summary`)이나 인기 제품(`top_products`)은 참고용으로 조회해 드릴 수 있습니다. 혹은 환불 데이터를 다룰 수 있는 전용 조회 도구가 추가되면 바로 확인해 드리겠습니다.
```