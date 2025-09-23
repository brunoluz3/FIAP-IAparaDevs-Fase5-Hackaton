from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from rag import semantic_search_STRIDE

load_dotenv()

def generate_stride_knowledge(content) -> ChatPromptTemplate:
    knowlodge_database = semantic_search_STRIDE.search_knowledge_STRIDE_database(content)
    prompt = ChatPromptTemplate.from_messages([
        """
            Você é um analista de segurança da informação e deve utilizar o seu conhecimento do metodo STRIDE para identificar 
            vulnerabilidades na solução apresentada e deve sugerir melhorias de forma direta e objetiva.

            Utilize o contexto abaixo para realizar a analise:

            {knowledge_STRIDE_base}
        """
    ])    
    
    formatted_prompt = prompt.format_prompt(knowledge_STRIDE_base=knowlodge_database)

    return formatted_prompt