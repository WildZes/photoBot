from sqlalchemy import Column, DateTime, Integer, ForeignKey, LargeBinary, String
from sqlalchemy.orm import relationship, backref
from data_base.dbcore import Base
from models.product import Products


class Orders(Base):

    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    description = Column(String)
    photo = Column(LargeBinary)
    about_contact = Column(String)
    contact = Column(String)
    data = Column(DateTime)

    def __str__(self):
        return f"{self.contact} {self.data}"
