from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SpyCat(Base):
    __tablename__ = "spy_cats"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    years_of_experience = Column(Float, nullable=False)
    breed = Column(String, nullable=False)
    salary = Column(Float, nullable=False)

    # Relationships
    mission = relationship("Mission", back_populates="cat")


class Mission(Base):
    __tablename__ = "missions"
    id = Column(Integer, primary_key=True, index=True)
    cat_id = Column(Integer, ForeignKey("spy_cats.id"), nullable=True)
    is_complete = Column(Boolean, default=False)

    # Relationships
    cat = relationship("SpyCat", back_populates="mission")
    targets = relationship("Target", back_populates="mission")


class Target(Base):
    __tablename__ = "targets"
    id = Column(Integer, primary_key=True, index=True)
    mission_id = Column(Integer, ForeignKey("missions.id"))
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    notes = Column(Text)
    is_complete = Column(Boolean, default=False)

    # Relationship
    mission = relationship("Mission", back_populates="targets")
