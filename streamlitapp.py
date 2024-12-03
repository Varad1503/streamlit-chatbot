import streamlit as st

from groq import Groq

import os
import json

#streamlit view config

st.set_page_config(
    page_title = "LLM Chat Project - Groq",
    layout="wide"
)

working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))

GROQ_API_KEY = config_data["GROQ_API_KEY"]
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

client = Groq()

# streamlit session state: chat histroy

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []



for message in st.session_state.chat_history:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

user_prompt = st.chat_input("Ask me anything..")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role" : "user", "content" : user_prompt})

    messages = [
        {"role" : "system", "content" : "You are a very help and sassy assitant"},
        *st.session_state.chat_history
    ]

    response = client.chat.completions.create(
        model = "llama-3.1-8b-instant" ,
        messages= messages
    )

    assistant_response = response.choices[0].message.content

    st.session_state.chat_history.append({"role" : "assistant", "content" : assistant_response})

    with st.chat_message("assistant"):
        st.markdown(assistant_response)
