import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import os

# Set the title of the Streamlit app
st.title("Gemini Chatbot")

# Initialize chat history in session state if it doesn't exist
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [SystemMessage(content="You are a helpful assistant.")]

# Initialize the LLM
def initialize_llm():
    """Initializes the ChatGoogleGenerativeAI model."""
    try:
        # Attempt to get the API key from Streamlit secrets
        api_key = st.secrets["GOOGLE_API_KEY"]
        return ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=api_key)
    except KeyError:
        # If the API key is not in Streamlit secrets, try to get it from the user's environment
        api_key = os.environ.get('GOOGLE_API_KEY')
        if api_key:
            return ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=api_key)
        else:
            #If no api key
            st.error("GOOGLE_API_KEY not found. Please set it as a Streamlit secret or environment variable.")
            return None

llm = initialize_llm()

# Display chat messages from history
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

# Get user input
if prompt := st.chat_input("You:"):
    st.session_state.chat_history.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get the AI response
    if llm: # check if llm is initialized
        result = llm.invoke(st.session_state.chat_history)
        st.session_state.chat_history.append(AIMessage(content=result.content))
        with st.chat_message("assistant"):
            st.markdown(result.content)
    else:
        st.stop() # stop if LLM is not initialized.
