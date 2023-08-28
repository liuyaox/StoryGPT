import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tables import Location

# Create the database engine
engine = create_engine('sqlite:///worlds.db')  # You can replace 'worlds.db' with your database name

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

st.title("Location Building Form")

# Form inputs for Location class
with st.form("add_location", clear_on_submit=True):
    location_name = st.text_input("Location Name", "")
    location_description = st.text_area("Location Description", height=400)

    submitted = st.form_submit_button("Submit")
    if submitted:
        new_location = Location(name=location_name, description=location_description)
        session.add(new_location)
        session.commit()
        st.success("Location added successfully!")



# Close the session when done
session.close()
