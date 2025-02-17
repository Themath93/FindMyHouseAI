""" 사용자의 정보를 확인하고 수정하는 Agent 모듈입니다. """

from typing import Annotated, Literal, Sequence, List
from typing_extensions import TypedDict

from langchain import hub
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field

from src.agent.model import get_openai_model
from src.graph.workflow import AgentState

from dotenv import load_dotenv
load_dotenv()

class UserInformation(BaseModel):
    """ 사용자의 정보를 저장하는 클래스입니다. """
    age: int = Field(description="사용자의 나이 (만 나이) 19 ~ 99")
    gender: str = Field(description="사용자의 성별 'male', 'female' 둘 중 하나만 가능")
    district: str = Field(description="사용자의 주민등록 시, 군 구 ex) '서울특별시 강남구'")
    married: bool = Field(description="사용자의 결혼 여부 'True' or 'False'")
    marriage_date: str = Field(description="사용자의 혼인신고 일자 ex) '2022-01-01'")
    income: int = Field(description="사용자의 소득 0 ~ 999999999 원 단위")  
    asset: int = Field(description="사용자의 자산 0 ~ 999999999 원 단위")
    has_car: bool = Field(description="사용자의 차량보유 여부 'True' or 'False'")
    car_value: int = Field(description="사용자의 차량가액 0 ~ 999999999 원 단위")
    budget: int = Field(description="사용자의 예산 0 ~ 999999999 원 단위")
    house_size: int = Field(description="사용자의 원하는 집 크기 0 ~ 999 제곱미터 단위(m2)")    
    price_limit: int = Field(description="사용자의 상한 가격 0 ~ 999999999 원 단위")
    rent_type: str = Field(description="사용자의 전세, 월세, 전체 '전세', '월세', '전체' 중 하나만 가능")
    is_data_collected: bool = Field(description="사용자의 정보가 수집되었는지 여부 'True' or 'False'")

class UserInformationChange(BaseModel):
    """ 사용자의 정보를 수정하는 클래스입니다. """
    
    change_column_list: List[dict] = Field(description="사용자의 정보를 수정할 컬럼 리스트 key: 변경할 컬럼명, value: 변경할 값 key 로 허용되는 값 : [age, gender, district, married, marriage_date, income, asset, has_car, car_value, budget, house_size, price_limit, rent_type]")
    is_done: bool = Field(description="사용자의 정보 수정이 완료되었는지 여부 'True' or 'False'")

def user_info_gather(state: AgentState) -> Literal["more_info", "done"]:
    """ 사용자의 정보를 수집하는 Agent 입니다. 
    
    Args:
        state (AgentState): AgentState 객체
    
    Returns:
        UserInformation: 사용자의 정보를 저장한 UserInformation 객체
    """
    
    model = get_openai_model()
    
    model_with_tool = model.with_structured_output(UserInformation)
    
    # prompt
    
    prompt = PromptTemplate(
        template="""당신은 사용자의 정보를 수집하거나 수정하는 Agent 입니다.
        주어진 사용자의 정보를 알맞게 가공해주세요.
        금액은 모두 KRW 단위로 대한민국의 화폐 단위입니다.
        나이는 만 나이로 입력받으세요.
        성별은 male 또는 female 만 허용됩니다.
        ** 받지못한 정보를 마음대로 생성하면 안됩니다. **
        필수로 받아야할 정보는 다음과 같습니다.
        - age(나이)
        - gender(성별)
        - district(주소)
        - married(결혼 여부)
            - marriage_date(혼인신고일) : 결혼을 했을 경우에만 필요합니다.
        - income(소득)
        - asset(자산)
        - has_car(차량 보유 여부)
            - car_value(차량 가격) : 차량을 보유하는 경우에만 필요합니다.
        - budget(예산)
        - house_size(원하는 집 크기)
        - price_limit(상한 가격)
        - rent_type(전세, 월세, 전체)
        - is_data_collected(정보 수집 여부)
            - 결혼 여부, 차량 가격은 결혼을 했을 경우, 차량을 보유하는 경우에만 필요합니다.
            
        여기 사용자의 input을 제공하겠습니다. : {input} \n
        
        반드시 필수 정보가 모두 수집된 경우에만 is_data_collected를 True로 설정해주세요.
        """,
        input_variables=["input"],
    )
    
    # Chain
    chain = prompt | model_with_tool
    
    input = state["input"]
    user_info = chain.invoke({"input": input})
    
    user_info_dict = user_info.model_dump()
    
    for key, value in user_info_dict.items():
        state[key] = value
    
    if user_info_dict["is_data_collected"] == False:
        return "more_info"
    else:
        return "done"
    

def user_info_confirm_and_modify(state: AgentState) -> Literal["more_info", "done"]:
    """ 사용자의 정보를 확인하고 수정하는 Agent 입니다. 
    
    Args:
        state (AgentState): AgentState 객체
    
    Returns:
        UserInformation: 사용자의 정보를 저장한 UserInformation 객체
    """
    
    model = get_openai_model()
    
    model_with_tool = model.with_structured_output(UserInformationChange)
    # prompt
    
    prompt = PromptTemplate(
        template="""당신은 사용자의 정보를 확인하고 수정하는 Agent 입니다.
        주어진 사용자의 정보를 확인하고 수정해주세요.
        ** 받지못한 정보를 마음대로 생성하면 안됩니다. **
        수정할 수 있는 컬럼명은 다음과 같습니다:
        - age(나이)
        - gender(성별)
        - district(주소)
        - married(결혼 여부)
            - marriage_date(혼인신고일) : 결혼을 했을 경우에만 필요합니다.
        - income(소득)
        - asset(자산)
        - has_car(차량 보유 여부)
            - car_value(차량 가격) : 차량을 보유하는 경우에만 필요합니다.
        - budget(예산)
        - house_size(원하는 집 크기)
        - price_limit(상한 가격)
        - rent_type(전세, 월세, 전체)
        - is_data_collected(정보 수집 여부)
            - 결혼 여부, 차량 가격은 결혼을 했을 경우, 차량을 보유하는 경우에만 필요합니다.
            
        여기 사용자의 input을 제공하겠습니다. : {input} \n
        사용자가 정보를 다 입력했다는 내용이 input 에 포함되어 있으면 is_done을 True로 설정해주세요.
        """,
        input_variables=["input"],
    )
    
    # Chain
    chain = prompt | model_with_tool
    
    input = state["input"]
    user_info = chain.invoke({"input": input})
    
    user_info_dict = user_info.model_dump()
    
    if user_info_dict["change_column_list"] != []:
        for change in user_info_dict["change_column_list"]:
            for key, value in change.items():
                state[key] = value
    
    if user_info_dict["is_done"] == False:
        return "more_info"
    else:
        return "done"