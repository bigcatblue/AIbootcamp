import streamlit as st

st.html("""<div style="text-align: center; font-size: 24px; color: #333; font-weight: bold; margin-bottom: 20px;">About us page</div>""")
st.html("""<h3>Problem Statement</h3>
<h4>The GovTech Bulk Tender for supply of ICT Specialist Augmented Resource (AR) is among highest utilised contract in GovTech. Current manual approach to prepare purchases against this Bulk Tender is taxing (on both users and procurement officers) and subjected to inaccuracy and contractual risk.</h4> 
<hr>
<h5>Project Scope</h5>
        
Among the purchase preparations are:
a) information gathering (e.g salient contractual info); and 
b) drafting of the Approval of Requirement (AOR) document.
<br>
<br>
<h5>Objectives</h5>
<br>
Using LLM, to develop a tool that, 
a) helps user to identify and extract of the salient contractual info for the AR (i.e rates) across the panel of contractors; and 
b) helps user in drafting the AOR in accordance with a built-in reference template to ensure key AOR considerations are addressed.
<br>
<br>
<h5>Data sources</h5>
<br>
a) Salient contractual info – Source: Bulk Tender contract rates (data are sanitised);
b) AOR drafter – Source: Bulk Tender contract rates (data are sanitised) & prescribed standard AOR template in the Bulk Tender’s contract admin guide.
<br>  
<br>        
<h5>Features</h5>

a) Salient contractual info – <br>
For the Job Role of interest, this tool can:<br>
    i.   identify the relevant contractors, <br>
    ii.  extract the corresponding rates for each and every of these contractors,<br>
    iii. offers insights (i.e most competitive rate) to facilitate decision making.<br>
<br>
<br>
b) AOR drafter – 
<br>  
        
This tool can provide structured prompts to guide user to address key AOR considerations:<br>
    i.   help user to derive a draft based on prescribed template which facilitates approval,<br>
    ii.  help user to summarise and craft the content which relieves editorial efforts,<br>
    iii. help user to strengthen their purchase justification for information they provided.<br>
<br>  
""")

