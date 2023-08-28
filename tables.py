from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    world_id = Column(Integer, ForeignKey('worlds.id'))

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    world_id = Column(Integer, ForeignKey('worlds.id'))

class McGuffin(Base):
    __tablename__ = 'mcguffins'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    world_id = Column(Integer, ForeignKey('worlds.id'))

class Character(Base):
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    world_id = Column(Integer, ForeignKey('worlds.id'))

class World(Base):
    __tablename__ = 'worlds'
    id = Column(Integer, primary_key=True)
    name= Column(String)
    Plot = Column(String)
    History = Column(String)
    magic_system = Column(String)
    
    locations = relationship('Location', backref='world', cascade='all, delete-orphan')
    groups = relationship('Group', backref='world', cascade='all, delete-orphan')
    mcguffins = relationship('McGuffin', backref='world', cascade='all, delete-orphan')
    characters = relationship('Character', backref='world', cascade='all, delete-orphan')


# Create the database engine
engine = create_engine('sqlite:///worlds.db')  # You can replace 'worlds.db' with your desired database name

# Create the tables in the database
Base.metadata.create_all(engine)