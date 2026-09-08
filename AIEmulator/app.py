# Import streamlit, langchain modules, OS, and dotenv file
import streamlit as st
from langchain_classic.chains import ConversationChain
from langchain_classic.memory import ConversationBufferMemory
from langchain_classic.llms import OpenAI
from langchain_classic.callbacks import get_openai_callback
from dotenv import load_dotenv
import os

# Initialize LLM object to utilize OpenAI key linked to secure.env file
load_dotenv()
llm = OpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))

# Setup conversation chain with memory
conversation = ConversationChain(
    llm=llm,
    memory=ConversationBufferMemory()
)

# Initialize components for the Streamlit UI
st.title("LangChain Chatbot")
user_input = st.text_input("You: ")

# Process user input and display response
if user_input:
    # Close callback method once finished using 'With' statement
    with get_openai_callback() as cb:
        # Receive user input and generate response from LangChain
        response = conversation.run(input=user_input)
        # Display response and token usage
        st.write(f"Bot: {response}")
        st.write(f"Tokens used: {cb.total_tokens}")