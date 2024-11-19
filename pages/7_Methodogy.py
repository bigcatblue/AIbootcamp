import streamlit as st
from PIL import Image

st.html("<h4>Team: Luo Yi Hua (PRCT), Sophia Siak (CSG), Kang Khong Beng (CIO Office)</h4>")

st.html("<h4>Methodology in creating the app")

st.html("""
<br>
        
<h5>Data classification</h5>
<br>
    The data fields required for ICT specialists Augmented Resource are Company, Role, Seniority and Cost per month. The data for cost per month used is generated by a random generator. The program is found in general_data.ipynb. Data storage is kept as a csv file and also a sqlite database on streamlit community cloud.
<br>
<br>
<h5>Process flow</h5>
<br>
The hiring of augment resource has the following general flow.
""")

process_flow = Image.open("data/process.png")
st.image(process_flow)

st.html("""

<br>
<br>
<h5>Pain points</h5>
    1.	In step 1. selection the resources from the list of tenders, user has to read several tenders submission that are in excel files and various tabs. 
<br>
    2.	Step 2, for user that is unfamiliar in creating AOR, a standard template is generated for user. 
<br>
<br>
<h5>Solution and methodology</h5>
<br>
    1.	Pain point 1, the app solves it by providing an easy way to query using natural language on the available resources instead of reading the excel files. CrewAI is used to help user query a database of company that supplied the resources and help analyze the data. 
    <br><br>&nbsp    a.	The first CrewAI agent, agent_SQL has a database export role and accepts user’s text and converts that into a SQL statement, and query an SQLite database for the requested data. 
    <br>&nbsp    b.	The second agent, agent_writer, has role as a writer and analyzes the data from Agent_SQL and provide an analysis for the user. 

<br><br>
    2.	Pain point 2, OpenAI, and Streamlit form components are used. There are two solutions to it.

        <br><br>i.	In AOR generator page, a prompt is created for the LLM to ask various questions for before creating a AOR that user can copy and submit for approval.
""")
LLM = Image.open("data/LLM.png")
st.image(LLM)

st.html("""        <br><br>ii.	In AOR generator page with forms page uses Streamlit’s form capabilities to guide the users to completing key data required for the AOR and use LLM to generate a justification and allow the AOR to be downloaded as a MS Word document. 
        """)
form_image = Image.open("data/Forms.png")
st.image(form_image)