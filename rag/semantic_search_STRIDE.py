from langchain_chroma.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

vector_database = "vector_STRIDE_database"

def search_knowledge_STRIDE_database(content):
    database = load_database()
    result = semantic_search(database, content)
    return result

def load_database():
    embedding_function = OpenAIEmbeddings()
    database = Chroma(persist_directory=vector_database, embedding_function=embedding_function)
    return database

def semantic_search(database: Chroma, content):
    search_results = database.similarity_search_with_relevance_scores(content, k=5)
    results = []
        
    for data in search_results:
        results.append(data[0].page_content)
    
    print(results)
    return "\n\n----\n\n".join(results)