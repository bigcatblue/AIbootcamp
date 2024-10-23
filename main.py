#Set up and run this Streamlit App
import streamlit as st
import pandas as pd
from helper_functions import llm
from logics.customer_query_handler import process_user_message


# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="Augement Resource Page"
)
# endregion <--------- Streamlit App Configuration --------->

st.title("Streamlit App for Augmented Resource")

st.write("This is a Streamlit App that demonstrates how to use the OpenAI API to generate SQL statement and analysis of the data. In the augmented resource page, there is a chatbot implemented using CrewAI that retrieves a list of augmented resources in a SQLite database.")
st.write("User enters a questions and an agent translate it to a SQL statement and queries the database.")
st.write("Another agent, writer will analyse the data and write an analysis")