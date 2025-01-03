from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey, Text
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from pydantic import BaseModel

Base = declarative_base()


class SportType(Base):
    __tablename__ = 'sport_type'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    unit = Column(String, nullable=False)  
    world_record = Column(Float, nullable=True) 
    olympic_record = Column(Float, nullable=True)  
    searchable_data = Column(String, nullable=False)   
    results = relationship('Result', back_populates='sport_type')

class SportTypeModel(BaseModel):
    name: str
    unit: str
    world_record: float | None
    olympic_record: float | None



class Athlete(Base):
    __tablename__ = 'athlete'

    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)  
    country = Column(String, nullable=False) 
    birth_year = Column(Integer, nullable=False)  
    victories = Column(Integer, nullable=False)  
    results = relationship('Result', back_populates='athlete')

class AthleteModel(BaseModel):
    full_name: str
    country: str
    birth_year: int
    victories: int



class Result(Base):
    __tablename__ = 'result'

    id = Column(Integer, primary_key=True)
    sport_type_id = Column(Integer, ForeignKey('sport_type.id'), nullable=False)
    athlete_id = Column(Integer, ForeignKey('athlete.id'), nullable=False)
    competition_name = Column(String, nullable=False) 
    result_value = Column(Float, nullable=False)  
    competition_date = Column(Date, nullable=False) 
    location = Column(String, nullable=False)  

    sport_type = relationship('SportType', back_populates='results')
    athlete = relationship('Athlete', back_populates='results')

class ResultModel(BaseModel):
    sport_type_id: int
    athlete_id: int
    competition_name: str
    result_value: float
    competition_date: str
    location: str



engine = create_engine('sqlite:///sports.db')
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    return SessionLocal()