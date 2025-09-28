from langchain_chroma.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

vector_database = "vector_STRIDE_database"

"""
    Esse metódo é responsável por orquestrar os outros metodos que carregam a base vetorizada em memória e 
    fazer a chamada da pesquisa semantica
"""
def search_knowledge_STRIDE_database(content):
    database = load_database()
    result = semantic_search(database, content)
    return result

"""
    Esse metódo é responsável carregar a base vetorial que está no disco para a memória da aplicação
"""
def load_database():
    embedding_function = OpenAIEmbeddings()
    database = Chroma(persist_directory=vector_database, embedding_function=embedding_function)
    return database

"""
    Esse metódo é responsável por fazer a pesquisa semantica na base vetorizada, ele recebe a base que foi carregada em memória mais
    o conteúdo da pesquisa que será executada
"""
def semantic_search(database: Chroma, content):
    search_results = database.similarity_search_with_relevance_scores(content, k=5)
    results = []
        
    for data in search_results:
        results.append(data[0].page_content)
    
    print(results)
    return "\n\n----\n\n".join(results)