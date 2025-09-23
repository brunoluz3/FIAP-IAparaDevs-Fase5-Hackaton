from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

def create_database():
    documents = document_loader()
    chunks = split_chunks(documents)
    create_vector_database(chunks)

def document_loader():       
    diretory = r"\base_STRIDE"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    files_path = script_dir + diretory

    loader = PyPDFDirectoryLoader(files_path, glob="*.pdf")
    documents = loader.load()
    return documents   

def split_chunks(documents):
    split_documents = RecursiveCharacterTextSplitter(
        chunk_size = 3000,
        chunk_overlap=500,
        length_function=len,
        add_start_index=True
    )

    return split_documents.split_documents(documents)

def create_vector_database(chunks):
    db = Chroma.from_documents(chunks, OpenAIEmbeddings(), persist_directory="vector_STRIDE_database") 

create_database()