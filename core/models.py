from sqlalchemy import Column, Integer, String, Text
from .database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    tech_stack = Column(String(200))
    link = Column(String(200))
    image_url = Column(String(200), default="default.jpg")
