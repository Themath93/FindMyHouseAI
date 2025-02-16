"""" Agent 가 동작하는 Langgraph Workflow 를 정의합니다. """


from typing import Annotated, Sequence
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """
    Agent 의 상태를 정의합니다.
    
    Args:
        messages: Agent 가 수신한 메시지 목록
        age: Agent 가 소통하는 사용자의 나이
        gender: Agent 가 소통하는 사용자의 성별
        district: Agent 가 소통하는 사용자의 주민등록 시, 군 구
        married: Agent 가 소통하는 사용자의 결혼 여부
        marriage_date: Agent 가 소통하는 사용자의 혼인신고 일자
        income: Agent 가 소통하는 사용자의 소득
        asset: Agent 가 소통하는 사용자의 자산
        has_car: Agent 가 소통하는 사용자의 차량보유 여부
        car_value: Agent 가 소통하는 사용자의 차량가액
        budget: Agent 가 소통하는 사용자의 예산
        house_size: Agent 가 소통하는 사용자의 원하는 집 크기
        price_limit: Agent 가 소통하는 사용자의 상한 가격
        rent_type: Agent 가 소통하는 사용자의 전세, 월세, 전체
    """
    messages: Annotated[Sequence[BaseMessage], add_messages]
    age: int
    gender: str
    district: str
    married: bool
    marriage_date: str
    income: int
    asset: int
    has_car: bool
    car_value: int
    budget: int
    house_size: int
    price_limit: int
    rent_type: str