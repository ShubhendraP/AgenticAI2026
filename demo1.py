import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langsmith import traceable

from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = ChatPromptTemplate.from_template(
    "You are a helpful assistant. Answer concisely. \n\n Question: {question}")

@traceable (run_type = "chain")
def ask_agent(question: str):
    chain = prompt | llm
    result = chain.invoke({"question": question})
    return result.content

if __name__ == "__main__":
    queries = (
        "Who discovered pencillin?"
        "Explain the difference between AI and Machine Learning."
        "What is the square root of 256?"
    )
    for query in queries:
        print(f"Question: {query}")
        answer = ask_agent(query)
        print(f"Answer: {answer}\n")
