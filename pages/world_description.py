import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tables import World, Location, Group, McGuffin, Character

# Import your classes here

# Create the database engine
engine = create_engine('sqlite:///worlds.db')  # You can replace 'worlds.db' with your database name

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

st.title("World Description")

# Display all worlds
st.header("Worlds")
world = session.query(World).first()

st.subheader(f"World Name: {world.name}")
st.write(f"Plot: {world.Plot}")
st.write(f"History: {world.History}")
st.write(f"Magic System: {world.magic_system}")
st.write("----------")

# Display all locations
st.header("Locations")
locations = session.query(Location).all()
for location in locations:
    st.subheader(f"Location Name: {location.name}")
    st.write(f"Location Description: {location.description}")
    st.write("----------")

# Display all McGuffins
st.header("McGuffins")
mcguffins = session.query(McGuffin).all()
for mcguffin in mcguffins:
    st.subheader(f"McGuffin Name: {mcguffin.name}")
    st.write(f"McGuffin Description: {mcguffin.description}")
    st.write("----------")

# Display all Characters
st.header("Characters")
characters = session.query(Character).all()
for character in characters:
    st.subheader(f"Character Name: {character.name}")
    st.write(f"Character Description: {character.description}")
    st.write("----------")

# Close the session when done
session.close()
