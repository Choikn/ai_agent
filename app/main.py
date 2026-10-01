'''
랭그래프기반 에이전트 실행하는 코드
'''
import asyncio
from app.agent.graph import build_graph

async def run(query: str):
    '''
        사용자 질문 => 랭그래프기반 에이전트 전달
    '''
    result = await build_graph().ainvoke(
         # 사용자 메세지를 구성(상태내 messages키값으로), 라운드(llm 호출회수) 0으로 세팅 => AgentState 기본구성하여 호출
        {"messages":[("user", query)], "rounds":0 },
        # 전체 순환 회수 제한 (18회는 설정)
        config = {"recursion_limit":18}
    ) # 초기 상태를 설정하여 그래프에게 전달