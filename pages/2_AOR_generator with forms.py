#Set up and run this Streamlit App
import streamlit as st
import pandas as pd
from openai import OpenAI
from helper_functions.llm import get_completion_by_messages
import docx
import io
# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="Streamlit Augmented Resource AOR App"
)
# endregion <--------- Streamlit App Configuration --------->

df_list = pd.read_csv("company_data.csv")
df_list.insert(0, 'Selected', [False]*len(df_list))

companies = df_list["Company"].unique().tolist()

with st.form("Select company"):
    company = st.multiselect("Select company", companies)
    submitted_company = st.form_submit_button("Submit")

with st.form("Select Resource"): 
    df_list = df_list[df_list["Company"].isin(company)]
    df_list["Duration"] = [12]*len(df_list)
    df_ar_resources = st.data_editor(df_list)
    submitted_resource = st.form_submit_button("Submit")

if submitted_resource:
    df_selected_resources = df_ar_resources[df_ar_resources["Selected"] == True]
    st.write(f"You have selected resources: {df_selected_resources}")
    st.session_state["selected_resources"] = df_selected_resources

with st.form("AOR Fields"):
    ao = st.text_input("Who is the AOR approving authority?")
    project = st.text_input("What is the project name?")
    agency = st.text_input("What is the beneficiary agency?")
    scope_of_ar = st.text_input("What is the scope of the AR?")
    funding = st.text_input("What is the funding source?")
    aor_submitted = st.form_submit_button("Generate Justification")

if aor_submitted:
    st.session_state["ao"] = ao
    st.session_state["project"] = project
    st.session_state["agency"] = agency
    st.session_state["scope_of_ar"] = scope_of_ar
    st.session_state["funding"] = funding

    st.write("AOR Approving Authority:", st.session_state.get("ao", "Not provided"))
    st.write("Project Name:", st.session_state.get("project", "Not provided"))
    st.write("Beneficiary Agency:", st.session_state.get("agency", "Not provided"))
    st.write("Scope of AR:", st.session_state.get("scope_of_ar", "Not provided"))
    st.write("Funding Source:", st.session_state.get("funding", "Not provided"))
    st.write("Selected Resources:")
    if "selected_resources" in st.session_state:
        st.write(st.session_state["selected_resources"])
    else:
        st.write("No resources selected")

    initial_prompt = """Create a justification for the AOR for the following resources: 
    {selected_resources}
    The AOR approving authority is: {ao}
    The project name is: {project}
    The beneficiary agency is: {agency}
    The scope of the AR is: {scope_of_ar}
    The funding source is: {funding}
    """  
    messages=[{"role": "system", "content": initial_prompt}]
    st.session_state["messages"] = messages
    response = get_completion_by_messages(messages)
    st.session_state["aor_text"] = response
    #st.write(response)

with st.form("Improve AOR"):
    if "aor_text" not in st.session_state:
        st.session_state["aor_text"] = "No text provided"

    aor_text_area = st.text_area("Draft Justification:", value=st.session_state["aor_text"], height=500)
    improve_button = st.form_submit_button("Improve")

    if improve_button:
        improve_message = "Please improve the following justification: " + aor_text_area
        messages = st.session_state["messages"]
        messages.append({"role": "user", "content": improve_message})
        response = get_completion_by_messages(messages)
        st.session_state["aor_text"] = response
        st.session_state["messages"].append({"role": "assistant", "content": response})
        #st.write(response)

if st.button("Export as Word Document"):
        doc = docx.Document()
        doc.add_paragraph(st.session_state["aor_text"])
        bio = io.BytesIO()
        doc.save(bio)
        st.download_button(label="Download Justification", data=bio.getvalue(), file_name="justification.docx")
        st.write("File saved as justification.docx")
        st.session_state["aor_text_to_save"] = aor_text_area


if st.button("Clear"):
    st.session_state.clear()
    st.rerun()
