from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class WishItem(Base):
    __tablename__ = 'wishlist'

    _id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    price = Column(Float)
    url = Column(String(1024))
    description = Column(String(1024))
