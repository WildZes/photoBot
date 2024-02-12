from sqlalchemy import Column, DateTime, Integer, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship, backref
from data_base.dbcore import Base
from models.category import Category


class Image(Base):

    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    data = Column(DateTime)
    img = Column(LargeBinary)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(
        Category,
        backref=backref('images',
                        uselist=True,
                        cascade='delete,all'))

    def __repr__(self):
        return f"{self.data} {self.category_id}"
