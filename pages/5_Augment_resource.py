import toml
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai_tools import tool
import sqlite3
import streamlit as st

with open(".streamlit/secrets.toml", "r") as f:
    secrets = toml.load(f)

os.environ['OPENAI_API_KEY'] = secrets['OPENAI_KEY']

@tool("SQLreader")
def readsqltable (query: str) -> str:
    """
    Reads a table from the SQLite database.

    Args:
        query (str): The SQL query to execute.

    Returns:
        None
    """
    # Connect to the SQLite database
    conn = sqlite3.connect('company_data.db')

    # Create a cursor object
    cur = conn.cursor()

    # Execute a query to select data from a table
    cur.execute(query)

    # Fetch all rows from the query
    rows = cur.fetchall()

    # Print the rows
    #for row in rows:
    #    print(row)

    # Close the connection
    conn.close()
    
    return rows


# Change the working directory to the current file's directory#
#os.chdir(os.path.dirname(os.path.abspath(__file__)))
#print(f"The current working directory is: {os.getcwd()}")

load_dotenv('.env')


agent_SQL = Agent(
    role="Database expert",
    goal="Generate an SQL statement for {question} based on the questions provided.",

    backstory="""
    You are a database expert, who is responsible for generating a database query for a specific database.
    """,
    allow_delegation=False, 
	verbose=True, 
)

agent_writer = Agent(
    role=" Writer",
    goal="Analyse the data from the SQL results. ",
    backstory="""Analyse the data generated from the SQL statement. """,
    allow_delegation=False, 
    verbose=True, 
)

task_sql = Task(
    description="""\
    1. The database has a table company_data with columns "company", "role", "seniority", and "cost"
    2. Ensure the accuracy of the SQL statment generated by checking the SQL statement against the table.
    3. Ensure the data generated will be informative.
    """,

    expected_output="""\
    Am accurate SQL statement that is correct.""",
    agent=agent_SQL, 
    tools=[readsqltable],
    context=[]
)

task_write = Task(
    description="""\
    1. Create the table of the input data generated by the database expert
    2. The data given is to assist in hiring of resources for projects. 
    3. Analyse the data through a comparing the data and providing insight using agent_SQL onlyt.
    """,

    expected_output="""
    An analysis of the data generated.""",
    agent=agent_writer,
)


crew = Crew(
    agents=[agent_SQL, agent_writer],
    tasks=[task_sql, task_write],
    verbose=True
)

result = crew.kickoff(inputs={"question": "I want to hire 2 Software Engineer for a project. Find the cheapest and give me the details."})


print(f"Raw Output: {result.raw}")
print("-----------------------------------------\n\n")
print(f"Token Usage: {result.token_usage}")
print("-----------------------------------------\n\n")
print(f"Tasks Output of Task 1: {result.tasks_output[0]}")
print("-----------------------------------------\n\n")
print(f"Tasks Output of Task 2: {result.tasks_output[1]}")
st.write_stream(result.tasks_output[0])
st.write_stream(result.tasks_output[1])