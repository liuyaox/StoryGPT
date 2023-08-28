import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tables import Character

# Import your classes here

# Create the database engine
engine = create_engine('sqlite:///worlds.db')  # You can replace 'worlds.db' with your database name

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()




st.title("Character Building Form")
with st.form("add_character", clear_on_submit=True):
    character_name = st.text_input("Character Name", "")
    character_description = st.text_area("Character Description", height=400)

    submitted = st.form_submit_button("Submit")
    if submitted:
        new_character = Character(name=character_name, description=character_description)
        session.add(new_character)
        session.commit()
        st.success("Character added successfully!")


    

# Close the session when done
