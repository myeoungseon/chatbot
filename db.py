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

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

database = Chroma(persist_directory="./database",
                  embedding_function=embeddings)

def delete_all(database):
    ids = database.get()['ids']
    for id in ids:
        database.delete(id)

df = pd.read_csv('qa_list.csv')

documents = [Document(page_content=row['QA'], metadata={'category': row['구분']}) for _, row in df.iterrows()]

delete_all(database)
database.add_documents(documents)

print(len(database.get()['ids']))