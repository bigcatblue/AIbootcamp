import streamlit as st
import pandas as pd
import json


# Load the JSON file
filepath = 'company_data.csv'
df_augmented_resources = pd.read_csv(filepath)
# display the `dict_of_course` as a Pandas DataFrame
st.write(df_augmented_resources)