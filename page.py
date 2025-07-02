import streamlit as st
from dotenv import dotenv_values
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage
import chromadb
from datetime import datetime


config = dotenv_values(".env")
from langchain_openai import AzureOpenAIEmbeddings

embeddings = AzureOpenAIEmbeddings(
    model="text-embedding-3-small",
    azure_endpoint=config.get("AZURE_EMBEDDING_ENDPOINT"),
    api_key=config.get("AZURE_EMBEDDING_API_KEY"),
)

ef = embeddings.embed_documents
st.title("This is a Chat App")

client = chromadb.HttpClient(host="8765")
if not (ret := client.heartbeat()):
    st.error("Chroma srever is down")
    st.stop()
else:
    st.write(f"Chroma time: {datetime.fromtimestamp(int(ret / 1e9))}")

collection = client.get_or_create_collection("EON")

groq_api_key = config["GROQ_API_KEY"]

if "llm" not in st.session_state:
    llm = ChatGroq(
        model = config["GROQ_MODEL"],
        api_key=groq_api_key,
        temperature=0.7,
        max_tokens = "none"
    )
else:
    llm = st.session_state.llm


if "messages" not in st.session_state:
    st.session_state.messages =[]

for message in st.session_state.messages:
    if isinstance(message,HumanMessage):
        with st.chat_message(message["user"]):
            st.write(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
           st.write(message.content)

def generate_response(msg: str):
    messages = st.session_state.messages
    response = llm.invoke(messages)
    st.session_state.messages.append(response)
    return response

if message := st.chat_message("Enter message"):
    st.session_state.messages.append(HumanMessage(content=msg))
    response = generate_response(msg)
    st.rerun()
