from data.database import db
from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, JSON
from sqlalchemy.orm import relationship


class UserTable(db.Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True, index=True)
    password_hash = Column(String(255), nullable=False)
    profile = relationship("UserProfile", back_populates="user")


class UserProfile(db.Base):
    __tablename__ = "user_profiles"
    profile_id = Column(Integer, primary_key=True)
    username = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    # Financial Information
    annual_salary = Column(Numeric(15, 2))
    monthly_takehome = Column(Numeric(15, 2))
    savings_amount = Column(Numeric(15, 2))
    retirement_savings = Column(Numeric(15, 2))

    # Personal Information
    age = Column(Integer)
    desired_retirement_age = Column(Integer)

    # Career and Education
    job_title = Column(String(100))
    company = Column(String(100))
    education_level = Column(String(100))
    field_of_study = Column(String(100))

    # Goals stored as JSONB for flexibility
    financial_goals = Column(JSON)

    # todo: figure out how to store credit statement
    # credit_statement = Column(JSON)
