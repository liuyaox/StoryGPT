import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from tables import World


# Create the database engine
engine = create_engine('sqlite:///worlds.db')  # You can replace 'worlds.db' with your desired database name

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

st.markdown("# World Building Form")

# Form inputs for World class
with st.form("my_form"):
    name= st.text_input("World Name", "")
    plot = st.text_area("Plot", height=200)
    history = st.text_area("History", height=600)
    magic_system = st.text_area("Magic System", height=600)

    submitted = st.form_submit_button("Submit")
    if submitted:
        new_world = World(name=name, Plot=plot, History=history, magic_system=magic_system)
        session.add(new_world)
        session.commit()
        st.success("World added successfully!")

# Close the session when done
session.close()
