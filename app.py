
from openai import OpenAI
import streamlit as st

api_key = st.secrets['OPENAI_API_KEY']
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage

st.markdown("# ChatGPT-like clone")

st.write("Title")

# Initialize LangChain ChatOpenAI instead of OpenAI client
llm = ChatOpenAI(
    api_key=api_key,
    model_name="gpt-3.5-turbo",
    streaming=True,
    temperature=0.7
)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new user input
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Convert messages to LangChain format
        langchain_messages = []
        for m in st.session_state.messages:
            if m["role"] == "user":
                langchain_messages.append(HumanMessage(content=m["content"]))
            elif m["role"] == "assistant":
                langchain_messages.append(AIMessage(content=m["content"]))
            elif m["role"] == "system":
                langchain_messages.append(SystemMessage(content=m["content"]))
        
        # Stream the response
        response = st.write_stream(llm.stream(langchain_messages))
    
    st.session_state.messages.append({"role": "assistant", "content": response})