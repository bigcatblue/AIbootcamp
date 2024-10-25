#__import__('pysqlite3')
import sys
#sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import toml
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from crewai_tools import tool
import sqlite3
import streamlit as st



def run_crewai_app(question):

    with open(".streamlit/secrets.toml", "r") as f:
        secrets = toml.load(f)

    os.environ['OPENAI_API_KEY'] = secrets['OPENAI_KEY']

    @tool("SQLreader")
    def readsqltable (query: str) -> str:
        """
        Reads a table from the SQLite database.

        Args:
            query (str): The SQL query to execute.
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
        You are an agent design to convert text to SQL statement. Given a question create a syntactically correct SQLite statement. Limit the statement to only the question asked
        If the is no value return, write the SQL statement again. 
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
        1. The database has a table company_data with columns "company", "role", "seniority", and "cost".
        2. Ensure the accuracy of the SQL statment generated by checking the SQL statement against the table.
        3. Ensure the data generated will be informative and only return columns that are in the table.
        4. If no data is returned, write the SQL statement again.
        5. the table rows are in lower case. check the the query to the table are all in lower case.
        """,

        expected_output="""\
        Am accurate SQL statement that is correct and a results that is not empty.""",
        agent=agent_SQL, 
        tools=[readsqltable],
        context=[]
    )

    task_write = Task(
        description="""\
        1. Create the table of the input data generated by the database expert
        2. The data given is to assist in hiring of resources for projects. Do not use any example data.
        3. Analyse the data through a comparing the data and providing insight using agent_SQL only.
        4. If required, query the table for the data by modifying the query from agent_SQL.
        5. Return no data if there is no SQL data available for analysis. Do not create data.
        """,
        context=[task_sql],
        expected_output="""An analysis of the data for the sql data.""",
        agent=agent_writer,
        tools=[readsqltable]
    )


    crew = Crew(
        agents=[agent_SQL, agent_writer],
        tasks=[task_sql, task_write],
        verbose=True
    )

    result = crew.kickoff(inputs={"question": question})

    return result

#"I want to hire 2 Software Engineer for a project. Find the cheapest and give me the details."

def main():
    st.title("Augmented resource chat bot.")

    # Create a text input field for the user to enter their message
    user_input = st.text_input("Ask me about the different resources and its cost")

    # Create a button to trigger the chat
    if st.button("Send"):
        # Use CrewAI's API to generate a response based on the user's input
        #result = run_crewai_app("I want to hire 2 software engineer for a project. Find the cheapest and give me the details.")
        result = run_crewai_app(user_input.lower())
        # Display the response to the user
        st.write(result.raw)
        st.write('Out put below is for testing only and will be removed in production')
        st.write(result.tasks_output[0])
        st.write(result.tasks_output[1])
        st.write_stream(result)
        

if __name__ == "__main__":
    main()

#print(f"Raw Output: {result.raw}")
#print("-----------------------------------------\n\n")
#print(f"Token Usage: {result.token_usage}")
#print("-----------------------------------------\n\n")
#print(f"Tasks Output of Task 1: {result.tasks_output[0]}")
#print("-----------------------------------------\n\n")
#print(f"Tasks Output of Task 2: {result.tasks_output[1]}")
#st.write(result.raw)
#st.write('Out put below is for testing only and will be removed in production')
#st.write_stream(result.tasks_output[1])