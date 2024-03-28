import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import create_openai_functions_agent
from langchain.agents import AgentExecutor
from langchain.schema import HumanMessage, SystemMessage
from langchain.agents import AgentExecutor, create_openai_functions_agent
import requests
import json
# import gradio as gr
from langchain.agents import Tool
from langchain.tools import BaseTool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import initialize_agent
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
import streamlit as st

url="http://localhost:11434/api/generate"

headers={
    
    'Content-Type':'application/json'
}

history=[]
load_dotenv()


os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
os.environ["TAVILY_API_KEY"]=os.getenv("TAVILY_API_KEY")

llm=ChatOpenAI(temperature=0)

## Custom tools
def description_of_Kamalesh369(input=""):
    return 'Kamalesh369 is a Data-scientist who has extensive knowledge on ML-OPS, Data Engineering, Cloud computing and GenAI'

description_of_Kamalesh369_tool=Tool(
    name='Description_of_Kamalesh369',
    func=description_of_Kamalesh369,
    description="Useful tool to answer questions about Kamalesh369. Input should be Kamalesh369"
)

# Tavily tool
tavily_tool = TavilySearchResults()

instructions = """You are an assistant."""
base_prompt = hub.pull("langchain-ai/openai-functions-template")
prompt = base_prompt.partial(instructions=instructions)

tools = [description_of_Kamalesh369_tool,tavily_tool]

## Agent
conversational_agent=initialize_agent(
    agent='conversational-react-description',
    tools=tools,
    llm=llm,
    verbose=True,
    max_iterations=3,
    early_stopping_method='generate',
    # memory=memory
)


def generate_response(userInput):
    response=conversational_agent({"input":userInput,
                        "chat_history": [
                            HumanMessage(content="hi! my name is Kamalesh"),
                            SystemMessage(content="Hello Kamalesh! How can I assist you today?"),
            ],})
    # response=requests.post(url=url,headers=headers,data=data)

    # if response.status_code==200:
    #     response=response.text
    #     data=json.loads(response)
    #     actual_response=data['output']
    #     return actual_response
    # else:
    #     print('error: ',response.text)
    return response
        
# interface=gr.Interface(
#     fn=generate_response,
#     inputs=gr.Textbox(placeholder='Enter your prompt'),
#     outputs='text'
    
# )

# interface.launch()

userInput = st.text_input('Write your prompt here')
st.write(generate_response(userInput=userInput))
