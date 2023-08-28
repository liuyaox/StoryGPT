import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tables import McGuffin

# Import your classes here

# Create the database engine
engine = create_engine('sqlite:///worlds.db')  # You can replace 'worlds.db' with your database name

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

st.title("McGuffin Building Form")

with st.form("add_mcguffin", clear_on_submit=True):
    mcguffin_name = st.text_input("McGuffin Name", "")
    mcguffin_description = st.text_area("McGuffin Description", height=400)

    submitted = st.form_submit_button("Submit")
    if submitted:
        new_mcguffin = McGuffin(name=mcguffin_name, description=mcguffin_description)
        session.add(new_mcguffin)
        session.commit()
        st.success("McGuffin added successfully!")

# Close the session when done
session.close()