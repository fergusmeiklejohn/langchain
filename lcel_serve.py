from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langserve import add_routes

import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv() 

# access the environment variables
langchain_tracing = os.getenv('LANGCHAIN_TRACING_V2')
langchain_api_key = os.getenv('LANGCHAIN_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')

# 1. Create a chat prompt template
system_prompt = "You are a helpful assistant that can translate the following into {language}: "
prompt_template = ChatPromptTemplate.from_messages([("system", system_prompt), "user", "{input}"])

# 2. Create model
model = ChatOpenAI(
    temperature=0.5,
    api_key=openai_api_key,
    model_name="gpt-3.5-turbo"
)

parser = StrOutputParser()
chain = prompt_template | model | parser

app = FastAPI(
    title="Icel Serve",
    description="A simple langchain API",
    version="0.1.0"
)

add_routes(app, chain, path="/translate")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)