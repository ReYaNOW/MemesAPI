from sqlalchemy import TIMESTAMP, Column, Integer, String, Text, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Memes(Base):
    __tablename__ = 'memes'

    id = Column(Integer, primary_key=True)
    image_name = Column(String(length=100))
    text = Column(Text)
    created_at = Column(TIMESTAMP(), default=func.now())
