from sqlalchemy import Column, String, Integer, Boolean
from data_base.dbcore import Base
from models.entrepreneur import Entrepreneurs


class Business(Base):

    __tablename__ = 'business'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    entrepreneur_id = Column(Integer, ForeignKey('entrepreneurs.id'))
    entrepreneur = relationship(
        Entrepreneurs,
        backref=backref('entrepreneurs',
                        uselist=True,
                        cascade='delete-orphan, all'))

    def __str__(self):
        return self.name