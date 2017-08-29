"""
Components of creating a database: Configuration, Class, Table, and Mapper
"""

# Configuration
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


# Class
class Restaurant(Base):
    # Table
    __tablename__ = 'restaurant'
    # Mapper
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)


class MenuItem(Base):

    __tablename__ = 'menu_item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    # relationship
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    @property
    def serialize(self):
        # returns object data in JSON format
        return {
            'name': self.name,
            'id': self.id,
            'course': self.course,
            'description': self.description,
            'price': self.price
        }


# more Configuration
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)
