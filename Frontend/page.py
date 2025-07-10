import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.documents import Document
from datetime import datetime
import chromadb
import os
from langchain_openai import AzureOpenAIEmbeddings
from functools import lru_cache

load_dotenv(".env")
embeddings = AzureOpenAIEmbeddings(
    model="text-embedding-3-small",
    azure_endpoint=os.getenv("AZURE_EMBEDDING_ENDPOINT"),
    api_key=os.getenv("AZURE_EMBEDDING_API_KEY"),
)

ef = embeddings.embed_documents
st.title("RAG chat app")

groq_api_key = os.getenv("GROQ_API_KEY")

client = chromadb.HttpClient(host="localhost", port=8765)
if not (ret := client.heartbeat()):
    st.error("Chroma server is down")
    st.stop()
else:
    st.write(f"Chroma time: {datetime.fromtimestamp(int(ret / 1e9))}")

collection = client.get_or_create_collection("EON-Reality_local")


system_message = SystemMessage(
    content=""" You are an assistant. Answer questions solely based on the provided documents. 
    If the documents don't contain enough information to answer, say so clearly. 
    Do not make up information or rely on external knowledge."""
)
if "latest_msgs_sent" not in st.session_state:
    st.session_state.latest_msgs_sent = []
if "file_path" not in st.session_state:
    st.session_state.file_path = None

if "llm" not in st.session_state:
    llm = ChatGroq(
        model=os.getenv("GROQ_MODEL"),
        api_key=groq_api_key,
        temperature=0.7,
        # max_tokens=40,
    )
    st.session_state.llm = llm
else:
    llm = st.session_state.llm


if "messages" not in st.session_state:
    st.session_state.messages = []

def get_relevant_docs(message: HumanMessage) -> list[Document]:
    res = collection.query(query_texts=[message.content], n_results=5)
    return [Document(page_content=doc) for doc in res["documents"][0]]

def generate_response(msg: str):
    relevant_docs = get_relevant_docs(HumanMessage(content=msg))
    combined_sys_message = f"""{system_message.content}

Use the following documents to answer the question:
{"\n".join(doc.page_content for doc in relevant_docs)}"""
    # combined_sys_message = system_message
    messages = [SystemMessage(content=combined_sys_message)] + st.session_state.messages
    response = llm.invoke(messages)
    st.session_state.messages.append(response)
    st.session_state.latest_msgs_sent = messages
    return response
            
for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.write(message.content)
        # Display retrieved docs for the latest user message
        if message == st.session_state.messages[-1]:
            with st.expander("Retrieved Documents"):
                res = collection.query(query_texts=[message.content], n_results=5)
                for doc in res["documents"][0]:
                    st.write(doc)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.write(message.content)

if st.button("Clear Chat History"):
    st.session_state.messages = []
    st.rerun()

@lru_cache(maxsize=100)
def cached_query(query_text: str) -> list[str]:
    res = collection.query(query_texts=[query_text], n_results=5)
    return res["documents"][0]

if msg := st.chat_input("Enter a message"):
    st.session_state.messages.append(HumanMessage(content=msg))
    response = generate_response(msg)
    st.rerun()
