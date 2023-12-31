from config.database import Base
from sqlalchemy import Column, Integer, String, Float 

class WorkOfArt(Base):
    __tablename__ = "work_of_arts"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    overview = Column(String)
    year = Column(Integer)
    rating = Column(Float)
    category = Column(String)
    # Artist
    # Gallery