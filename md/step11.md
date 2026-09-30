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
---
agentlab=# \dt
             List of relations
 Schema |       Name        | Type  | Owner 
--------+-------------------+-------+-------
 public | demo_vectors      | table | agent
 public | document_chunks   | table | agent
 public | documents         | table | agent
 public | orders            | table | agent
 public | products          | table | agent
 public | schema_migrations | table | agent
(6 rows)

agentlab=# select * from products;
 product_id |    product_name     |  category  |   price    |   cost    
------------+---------------------+------------+------------+-----------
          1 | AI 업무자동화 Basic | software   |   49000.00 |  12000.00
          2 | AI 업무자동화 Pro   | software   |   99000.00 |  25000.00
          3 | 데이터 분석 패키지  | service    |  150000.00 |  50000.00
          4 | 사내 AI Agent 구축  | consulting | 1200000.00 | 500000.00
          5 | RAG 구축 컨설팅     | consulting |  800000.00 | 320000.00
(5 rows)

agentlab=# select * from orders;
 order_id |       order_date       | product_id | quantity |   amount   |  status  
----------+------------------------+------------+----------+------------+----------
        1 | 2026-09-01 01:00:00+00 |          1 |        3 |  147000.00 | paid
        2 | 2026-09-01 04:00:00+00 |          2 |        2 |  198000.00 | paid
        3 | 2026-09-02 02:20:00+00 |          3 |        1 |  150000.00 | paid
        4 | 2026-09-02 06:10:00+00 |          2 |        4 |  396000.00 | paid
        5 | 2026-09-03 00:30:00+00 |          4 |        1 | 1200000.00 | paid
        6 | 2026-09-03 05:30:00+00 |          1 |        5 |  245000.00 | paid
        7 | 2026-09-04 01:15:00+00 |          5 |        1 |  800000.00 | paid
        8 | 2026-09-04 08:00:00+00 |          2 |        1 |   99000.00 | refunded
        9 | 2026-09-05 03:00:00+00 |          3 |        3 |  450000.00 | paid
(9 rows)
```

# 실행
```
python -m steps.step11_tools
---
revenue=3586000.00, orders=8, range=2026-09-01~2026-09-05
1. 사내 AI Agent 구축: qty=1, revenue=1200000.00
2. RAG 구축 컨설팅: qty=1, revenue=800000.00
3. 데이터 분석 패키지: qty=4, revenue=600000.00
[source=HR-LEAVE-2026 | hybrid=0.382]
# 연차휴가 운영 규정

연차휴가는 직원의 휴식과 업무 지속 가능성을 보장하기 위한 제도이며, 직원은 부여된 휴가 범위에서 연차를 신청할 수 있다.입사 1년 미만 직원은 근로한 기간과 사내 운영 기준에 따라 현재 사용할 수 있는 휴가 일수를 인사 시스템에서 확인한 후 신청한다.

[source=HR-LEAVE-2026 | hybrid=0.207]
사용하지 않은 연차의 처리 방식은 관계 법령과 회사의 연차 운영 정책을 따른다. 회사가 연차 사용 촉진 절차를 운영하는 경우 인사팀은 대상 직원에게 사용 가능한 연차와 사용 기한을 안내한다. 직원은 안내된 기한 내에 휴가 계획을 확인하고 필요한 일정을 사전에 조정한다.

...
```