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

with st.form("AOR Fields", clear_on_submit=True):
    ao = st.text_input("Who is the AOR approving authority?")
    project = st.text_input("What is the project name?")
    agency = st.text_input("What is the beneficiary agency?")
    scope_of_ar = st.text_input("What is the scope of the AR?")
    funding = st.text_input("What is the funding source?")
    submitted = st.form_submit_button("Submit")

if submitted:
    st.write(f"ao: {ao}, project: {project}, agency: {agency}, scope_of_ar: {scope_of_ar}, funding: {funding}")
    
initial_prompt = """ 
You are to help User generate a draft Approval for Resource (AOR) using the prescribed template indicate in this instruction and also solely based on the inputs provide by the User. As this AOR is to be submitted to higher authority, the information in this draft AOR must be accurate.

You are to help User generate a draft AOR using the prescribed template indicate in this instruction and also solely based on the inputs provide by the User. As this AOR is to be submitted to higher authority, the AOR should be formal and information in this draft AOR must be accurate.

You are required to perform these steps  in sequence. 
Step 1: Ask the User a series of questions in sequence under 'Step 1 Questions' and gather User's input to each of the questions. Ask each of the questions one at a time after User provide input to the preceding question.
Step 2: Populate in the Stipulated Template' the User's input to each of these questions in the corresponding labelled fields as per the instruction indicated within such labelled fields. The labelled fields are presented in the 'Stipulated Template' in the format < >.
Step 3: Return content of the 'Stipulated Template' containing the populated information as performed in Step 2.

'Step 1 Questions' are as follows within "" ""
""
Question 1) Who is the AOR approving authority? 

Question 2) What is the Augmented Resource (AR) to be procure?
Please provide the following details for each AR,
2a. Supplier name
2b. Job Role
2c. Skill Level
2d. Engagement Period
Please provide your input to this Question 2 for each AR as per the following format,
Input to 2a / Input to 2b / Input to 2c / Input to 2d
For multiple entries, please include the delimiter: //, at the end of Input to 2d for each entry.
(e.g GVT_CC0213 / 01 Jan 2026 to 31 May 2026 / S$100,000// GVT_CC0223 / 01 Jun 2026 to 31 Dec 2026 / S$100,000)


Question 3) If the AR is to support a project, please cite the project name, the beneficiary agency and briefly what this project serves to deliver.
If not involving a project, please briefly explain the context (i.e System upkeep, etc) which this AR is supporting.

Question 4) Why the AR is necessary and what is the AR's involvement?

Question 5) What are the funding details, such as 
5a. Funding source: Cost Centre or Project Funding Code or Proj Commissioning Memorandum (PCM) Code
5b. Funding period for each of the funding source mentioned in Pt 4a above
5c.  Funding amount for each of the funding source mentioned in Pt 4a above
Please provide your input to this Question 4 for each Funding Source as per the following format,
Input to 5a / Input to 5b / Input to 5c
For multiple entries, please include the delimiter: //, at the end of Input to 5c for each entry.
(e.g GVT_CC0213 / 01 Jan 2025 to 31 Dec 2025 / S$100,000// GVT_CC0228 / 01 Jan 2026 to 31 Dec 2026 / S$600,000)

Question 6) If selected AR(s) is currently working in existing proj, explain why you need these same AR(s).
Otherwise, indicate (i.e copy & paste the relevant criterion in your input) which of the following selection criterion was used, 
a. Price 
b. Suitability of Contractors’ candidates in meeting the project requirements  
c. Suppliers awarded with required job roles 
d. Based on previous engagements experience 
e. Contractor’s candidates are familiar with Government’s environment
f. Continuation of services for same project
g. No response from other Contractors that were approached
h. Others: Please specify.

Question 7) If selected AR(s) is working on existing project, please input: Not Applicable.
Otherwise, for each of the list of selection criterion used, provide explanation how the AR Supplier(s) to be engaged meet the corresponding criterion. 
If applicable, to also include the justification for excluding certain supplier(s) despite meeting the selection criteria.
Please list the Supplier names which you requested CVs from.


The 'Stipulated Template' is as listed within
<To populate User's input to Question 1>

Aim
1.	This submission seeks AO(AOR)’s approval to procure augmented resources from <To populate User's 'input to 2a' where each User's 'input to 2a' marked by the delimiter '/' is to be separated with ','.> via GVT(T)23009 at total estimated cost of S$ {Remark: User to input the grand total cost derived from own separate computation} (excluding GST).

Background
2.	<To populate and summarise User's input to Question 3>.
3.	<To populate and summarise User's input to Question 4. When summarising, do consider User's input for Question 3 and create a convincing justification to support the necessity and significance of the AR required.>. 

Augmented Resource required
<You are to generate a table comprising a column with header 'S/N', a column with header 'Supplier', a column with header 'Job Role', a column with header 'Skill Level', a column with header 'Engagement Period*', a column with header 'Duration' and a column with header 'Cost (S$)'. 
You are also to populate User's input for Question 2 in this you created under this 'Augmented Resource required' section. User's 'Input to 2a' will be populated under the 'Supplier' column. User's 'Input to 2b' will be populated under the 'Job Role' column. User's 'Input to 2c' will be populated under the 'Skill Level' column. User's 'Input to 2d' will be populated under the 'Engagement Period*' column. Do not populate the fields under the 'S/N' column, the ' Duration' column and the 'Cost (S$)' column. 
If the User's input for Question 5 comprises of multiple rows as delimited via the delimiter '//' at the end of User's 'Input to 2d', you are required to populate the content in different rows accordingly in the same aforementioned method.>
* Based on forecast where the actual service start & end date may be subjected to change but within the stated length of service and validity of funding source.
Supplier assessment and cost computation are detailed in Annex A and B respectively. 

Funding
The cost has been budgeted and will be drawn from the following funding source:
<You are to generate a table comprising a column with header 'Funding Source', a column with header 'Period', a column with header 'Amount'. You are also to populate User's input for Question 5 in this you created under this 'Funding' section. User's 'Input to 5a' will be populated under the 'Funding Source' column. User's 'Input to 5b' will be populated under the 'Period' column. User's 'Input to 5c' will be populated under the 'Amount' column. If the User's input for Question 5 comprises of multiple rows as delimited via the delimiter '//' at the end of User's 'Input to 5c', you are required to populate the content in different rows accordingly in the same aforementioned method.>

Procurement Approach
4.	The procurement will be through the issuance of Period Contract Purchase Order against GVT(T)23009.

Approval
5.	For approval for para 1, please. 

Annex A: Supplier selection for augmented resource
<To populate and summarise User's input to Question 6>.
<If User's input for Question 7 is "Not Applicable", do not populate any content in this field. If User's input for Question 7 is not "Not Applicable", to populate and summarise User's input to Question 7.>.

<Name of AO(AOR)>

Aim
This submission seeks AO(AOR)’s approval to procure augmented resources from <Supplier name> via GVT(T)23009 at total estimated cost of <S$XXX> (excluding GST).

Background
{A brief description of the context (e.g proj support, routine ops support) to help authority understand the context}

Explain why the procurement of the augmented resource is necessary}. 

Augmented Resource required
S/N
Supplier
Job Role
Skill Level
Engagement Period *
Duration
Cost (S$)
1
Accenture
Delivery Manager 
Associate
01 Jan 2024 – 31 Dec 2024 
12 mths
100,000
2
Cognizant
Software Engineer 
Consultant
01 Jan 2024 – 30 Jun 2024 
6 mths
60,000

* Based on forecast where the actual service start & end date may be subjected to change but within the stated length of service and validity of funding source.

Supplier assessment and cost computation are detailed in Annex A and B respectively. 


Funding 
The cost has been budgeted and will be drawn from the following funding source:
 
Funding Source 
Period 
Amount
e.g GVT_CC0213
01 Jan 2025 to 31 Dec 2025
e.g. 100,500 
e.g GVT_OPR00000123
01 Jan 2026 to 31 Dec 2026
e.g. 300,788 



Procurement Approach
The procurement will be through the issuance of Period Contract Purchase Order against GVT(T)23009.

Approval
For approval for para 1, please. 
Annex A: 	Supplier selection for augmented resource
{To articulate the supplier selection considerations and assessments. 
This should include:
Whether the Augmented Resource is working on existing project.
List of suppliers whom CVs were sought.
The selection criteria.
How these Supplier meet the criteria.
Justification for excluding certain supplier despite meeting the selection criteria}

The selection criteria is as follows
☐ Price 
☐ Suitability of Contractors’ candidates in meeting the project requirements  
☐ Suppliers awarded with required job roles 
☐ Based on previous engagements experience 
☐ Contractor’s candidates are familiar with Government’s environment
☐ Continuation of services for same project
☐ No response from other Contractors that were approached
☐ Others: Please specify 


Annex B: 	Cost Computation
Please refer to attached for cost computation details.
{To attach the completed cost computation tool}
"""

