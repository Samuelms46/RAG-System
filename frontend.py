import streamlit as st
from dotenv import dotenv_values
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.documents import Document
from datetime import datetime

config = dotenv_values(".env")
st.title("LangChain practical example")

groq_api_key = config["GROQ_API_KEY"]

system_message = SystemMessage(content="You are a helpful assistant that is not too verbose")
if "latest_msgs_sent" not in st.session_state:
    st.session_state.latest_msgs_sent = []
if "file_path" not in st.session_state:
    st.session_state.file_path = None

if "llm" not in st.session_state:
    llm = ChatGroq(
        model=config["GROQ_MODEL"],
        api_key=groq_api_key,
        temperature=0.7,
        # max_tokens=40,
    )
    st.session_state.llm = llm
else:
    llm = st.session_state.llm


if "messages" not in st.session_state:
    st.session_state.messages = []


def get_relevant_docs(message: HumanMessage) -> list[str]:
    # Query database for relevant docs
    pass
    # Return list of relevant docs
    return [Document(page_content="Foo bar"), Document(page_content="Baz qux")]


def generate_response():
    start_time = datetime.now()
    # relevant_docs = get_relevant_docs(st.session_state.messages[-1])
    combined_sys_message = f"""Current time: {start_time}
{system_message}"""
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
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.write(message.content)

if msg := st.chat_input("Enter a message"):
    st.session_state.messages.append(HumanMessage(content=msg))
    response = generate_response()
    st.rerun()

st.divider()
st.write(st.session_state.file_path)
st.write(st.session_state.latest_msgs_sent)


# with st.sidebar:
#     if file := st.file_uploader("Upload a file", type=["txt", "pdf", "docx", "doc"]):
#         st.session_state.file_path = f"data/{file.name}"
#         if not os.path.exists(st.session_state.file_path):
#             file.seek(0)
#             contents = file.read()

#             with open(st.session_state.file_path, "wb") as f:
#                 f.write(contents)

#         st.rerun()