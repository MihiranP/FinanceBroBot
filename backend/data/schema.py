from data.database import db
from sqlalchemy import Column, ForeignKey, Integer, LargeBinary, Numeric, String, JSON
from sqlalchemy.orm import relationship


class UserTable(db.Base):
    __tablename__ = "users"
    username = Column(String, index=True)
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    password_hash = Column(String(255), nullable=False)
    profile = relationship("UserProfile", back_populates="user", uselist=False)


class UserProfile(db.Base):
    __tablename__ = "user_profiles"
    profile_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
    )
    user = relationship("UserTable", back_populates="profile")

    name = Column(String(100))
    annual_salary = Column(Numeric(15, 2))
    monthly_takehome = Column(Numeric(15, 2))
    savings_amount = Column(Numeric(15, 2))
    retirement_savings = Column(Numeric(15, 2))
    debt = Column(Numeric(15, 2))
    dependents = Column(Integer)
    age = Column(Integer)
    desired_retirement_age = Column(Integer)

    job_title = Column(String(100))
    company = Column(String(100))
    education_level = Column(String(100))

    state = Column(String(100))
    financial_goals = Column(JSON)
    investment_experience = Column(String(100))
    credit_statement = Column(JSON)

    podcasts = relationship("Podcasts", back_populates="user_profile")
    lessons = relationship("LessonPlans", back_populates="user_profile")


class Podcasts(db.Base):
    __tablename__ = "podcasts"
    podcast_id = Column(Integer, primary_key=True, autoincrement=True)
    user_profile_id = Column(Integer, ForeignKey("user_profiles.profile_id"))
    user_profile = relationship("UserProfile", back_populates="podcasts")
    raw_file = Column("file_data", LargeBinary)
    transcript = Column("transcript", String)


class LessonPlans(db.Base):
    __tablename__ = "lesson_plans"
    lesson_plan_id = Column(Integer, primary_key=True, autoincrement=True)
    user_profile_id = Column(Integer, ForeignKey("user_profiles.profile_id"))
    user_profile = relationship("UserProfile", back_populates="lessons")
    transcript = Column("transcript", String)
