from sqlalchemy import Column, String, Integer, Boolean
from data_base.dbcore import Base


class Entrepeneurs(Base):
    __tablename__ = 'entrepreneurs'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, unique=True)

    def __str__(self):
        return self.name