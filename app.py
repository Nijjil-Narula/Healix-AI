import os
from dotenv import load_dotenv
from flask import Flask, render_template, request

from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import (
    create_stuff_documents_chain,
)
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_pinecone import PineconeVectorStore
from src.helper import download_hugging_face_embeddings
from src.prompt import system_prompt

app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

if PINECONE_API_KEY:
    os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
if GROQ_API_KEY:
    os.environ["GROQ_API_KEY"] = GROQ_API_KEY

embeddings = download_hugging_face_embeddings()

index_name = "healthwise-chatbot"
# Embed each chunk and upsert the embeddings into your Pinecone index.
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

retriever = docsearch.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 8}
)

chatModel = ChatGroq(model="openai/gpt-oss-20b")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(chatModel, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)


@app.route("/")
def index():
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    if request.is_json:
        data = request.get_json() or {}
        msg = data.get("msg", "")
        history_payload = data.get("history", [])
    else:
        msg = request.form.get("msg", "")
        history_payload = []
    
    if not msg:
        return "No message provided", 400

    chat_history = []
    for item in history_payload:
        role = item.get("role", "")
        content = item.get("content", "")
        if role in ("user", "human"):
            chat_history.append(HumanMessage(content=content))
        elif role in ("assistant", "bot", "ai"):
            chat_history.append(AIMessage(content=content))

    response = rag_chain.invoke({"input": msg, "chat_history": chat_history})
    return str(response["answer"])


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
