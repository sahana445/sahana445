import streamlit as st
import os
os.environ["GOOGLE_API_KEY"]=st.secrets["GOOGLE_API_KEY"]
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# Title
st.title("💬 Gemini Chat - Streamlit")

# Sidebar for API key input
api_key = st.sidebar.text_input("Enter your Google API Key", type="password")

# Store chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [SystemMessage(content="You are a helpful assistant.")]

# Initialize LLM if API key is provided
if api_key:
    os.environ["GOOGLE_API_KEY"] = api_key
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

    # User input
    user_input = st.text_input("You:", key="input")

    if user_input:
        st.session_state.chat_history.append(HumanMessage(content=user_input))

        # Get LLM response
        with st.spinner("Thinking..."):
            result = llm.invoke(st.session_state.chat_history)
            st.session_state.chat_history.append(AIMessage(content=result.content))

    # Display chat history
    for msg in st.session_state.chat_history:
        if isinstance(msg, HumanMessage):
            st.markdown(f"**You:** {msg.content}")
        elif isinstance(msg, AIMessage):
            st.markdown(f"**AI:** {msg.content}")
else:
    st.warning("Please enter your Google API Key in the sidebar.")

