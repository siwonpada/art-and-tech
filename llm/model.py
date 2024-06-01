from langchain_openai import OpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

# OpenAI LLM 초기화
llm = OpenAI(
    temperature=0.7
)


class LLMResult(BaseModel):
    result: str = Field(description="사용자의 입력에 대한 대답")
    emotion: str = Field(description="사용자의 입력을 들을 사람이 느낄 감정")


output_parser = JsonOutputParser(pydantic_object=LLMResult)

format_instructions = output_parser.get_format_instructions()

template = """
## About Me
나는 지금까지의 대화와 사용자의 입력을 토대로 그에 맞는 대답을 해 준다.
또한, 사용자의 입력을 받은 사람이 느낄 감정을 예측한다.

## User input
사용자의 입력: {user_input}
지금까지의 대화: {context}

{format_instructions}
"""
prompt = PromptTemplate(
    template=template,
    input_variables=["user_input", "context"],
    partial_variables={"format_instructions": format_instructions}
)

llm_chain = prompt | llm | output_parser
