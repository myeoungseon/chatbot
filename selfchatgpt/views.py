from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory, ChatMessageHistory

import json

# Chroma 데이터베이스 초기화
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
database = Chroma(persist_directory="./database", embedding_function=embeddings)
chat_model = "gpt-3.5-turbo"

def index(request):
    return render(request, 'selfgpt/index.html')

def chat(request):
    if request.method == "POST":
        # Post로 받은 question을 가져옴
        query = request.POST.get('question')

        # 세션에서 대화 히스토리를 가져옴 (없으면 빈 리스트)
        chat_history = request.session.get('chat_history', [])
        
        # 대화 히스토리를 HumanMessage와 AIMessage 객체로 변환
        messages = []
        for msg in chat_history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "ai":
                messages.append(AIMessage(content=msg["content"]))

        # 대화 메모리 생성 및 히스토리 설정
        memory = ConversationBufferMemory(memory_key="chat_history", input_key="question", output_key="answer",
                                          return_messages=True)
        memory.chat_memory.messages = messages

        # ConversationalRetrievalQA 체인 생성
        k = 3
        retriever = database.as_retriever(search_kwargs={"k": k})
        chat = ChatOpenAI(model=chat_model)
        qa = ConversationalRetrievalChain.from_llm(llm=chat, retriever=retriever, memory=memory,
                                                   return_source_documents=True, output_key="answer")

        # 질의에 대한 결과를 가져옴
        result = qa({"question": query})

        # 대화 히스토리를 업데이트
        chat_history.append({"role": "user", "content": query})
        chat_history.append({"role": "ai", "content": result["answer"]})
        request.session['chat_history'] = chat_history

        context = {
            'question': query,
            'result': result["answer"],
            'chat_history': chat_history,
        }

        # DEBUG
        print(chat_history)
        print('---------------')
        print(memory.load_memory_variables({}))

        # 응답을 보여주기 위한 html 선택 (위에서 처리한 context를 함께 전달)
        return render(request, 'selfgpt/index.html', context)
    else:
        clear_chat(request)
        return render(request, 'selfgpt/index.html')
    
def clear_chat(request):
    if 'chat_history' in request.session:
        del request.session['chat_history']