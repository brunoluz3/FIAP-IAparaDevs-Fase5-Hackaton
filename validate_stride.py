from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from rag import rag_STRIDE

load_dotenv()

def validate_stride(content):
    model = ChatOpenAI()
    prompt = rag_STRIDE.generate_stride_knowledge(content)

    result = model.invoke(prompt)
    return result.content