#Set up and run this Streamlit App
import streamlit as st
import pandas as pd
from openai import OpenAI

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="Streamlit Augmented Resource AOR App"
)
# endregion <--------- Streamlit App Configuration --------->

st.title("I can help draft an AOR for augmented resources")

client = OpenAI(api_key=st.secrets["OPENAI_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#seed the first prompt
initial_prompt = """ 
You are a writer that is able to generate a approval for a request (AOR) for augmented resources. 
The request for approval should be based on the following details:
1. How many resources are needed
2. Cost of the resources
3. What is the purpose of the resources
4. What is the expected time to complete the project
5. Reasons for choosing this company for the augment resource
                """

st.session_state.messages.append({"role": "assistant", "content": initial_prompt})

if prompt := st.chat_input("Enter the augmented resource details?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

