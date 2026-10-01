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

    )