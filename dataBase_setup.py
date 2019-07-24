import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Categories(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    items = relationship('Items')

    # We added this serialize function to be able to send JSON objects in a
    # serializable format
    @property
    def serialize(self):

        return {
            'id': self.id,
            'name': self.name,
        }
    

class Items(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String, nullable = False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    categories = relationship(Categories)

# We added this serialize function to be able to send JSON objects in a
# serializable format
    @property
    def serialize(self):

        return {
            'item': self.name,
            'description': self.description,
            'id': self.id,
            'category_id': self.category_id
        }


# engine = create_engine('postgresql://vagrant:@localhost/categoriesitem')
engine = create_engine('sqlite:///categoriesitem.db')


Base.metadata.create_all(engine)