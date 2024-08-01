import pandas as pd
import numpy as np
import os
import sqlite3
from datetime import datetime
 
import openai
 
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, Document
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
 
from .models import *
 
# csv to sqlite
def csv_to_sqlite(csv_file_path):
    df = pd.read_csv(csv_file_path)
    for index, row in df.iterrows():
        content = row['QA']
        category = row['구분']  # CSV 파일의 '구분' 열을 category로 사용
        vector = Vector.objects.create(content=content, category=category)
        vector.save()
       
# sqlite_to_chroma
def reset_chunk_db():
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    database = Chroma(persist_directory="./database", embedding_function=embeddings)
 
    def delete_all(database):
        ids = database.get()['ids']
        for id in ids:
            database.delete(id)
 
    # todo: get sqlite
    vectors = Vector.objects.all()
 
    documents = [Document(page_content=vector.content, metadata={'category': vector.category}) for vector in vectors]
 
    delete_all(database)
    database.add_documents(documents)
 
    print(len(database.get()['ids']))