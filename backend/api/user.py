from fastapi import APIRouter, Depends
from pydantic import BaseModel
from data.schema import UserProfile, UserTable
from core.user import UserFinancialProfile, User
from typing import Annotated
from data.database import db
from sqlalchemy.orm import joinedload
from visibility.logging import logger
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(prefix="/users", tags=["user"])
DB = Annotated[db.SessionLocal, Depends(db.get_db)]


class PodcastResponse(BaseModel):
    podcast_id: int
    transcript: str | None

    class Config:
        from_attributes = True


class LessonPlanResponse(BaseModel):
    lesson_plan_id: int
    transcript: str | None

    class Config:
        from_attributes = True


class UserProfileResponse(BaseModel):
    profile_id: int
    name: str | None
    annual_salary: float | None
    monthly_takehome: float | None
    savings_amount: float | None
    retirement_savings: float | None
    debt: float | None
    dependents: int | None
    age: int | None
    desired_retirement_age: int | None
    job_title: str | None
    company: str | None
    education_level: str | None
    state: str | None
    financial_goals: list | None
    investment_experience: str | None
    podcasts: list[PodcastResponse] = []
    lessons: list[LessonPlanResponse] = []

    class Config:
        from_attributes = True


class UserFullResponse(BaseModel):
    user_id: int
    username: str
    profile: UserProfileResponse | None = None

    class Config:
        from_attributes = True


@router.put("/user")
async def save_user(username: str, password: str, db: DB):
    user = User(username=username, password=password)
    try:
        return await user.save_user_to_db(db)
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {e}"}


@router.put("/profile")
async def save_user_profile(userprofile: UserFinancialProfile, user_id: int, db: DB):
    try:
        ufp = UserFinancialProfile()
        validated_profile = userprofile.model_dump()
        return await ufp.save_user_profile(validated_profile, db, user_id)
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {e}"}


# TODO: Auth?? Maybe? Manav that's all you (I know it'll have to be me you lazy dog)
@router.get("/user/{user_id}", response_model=UserFullResponse)
async def get_user_data(user_id: int, db: DB):
    """
    Retrieve a user's complete data including their profile, podcasts, and lesson plans.
    The endpoint uses eager loading to fetch all related data in a single database query.
    """
    try:
        user = (
            db.query(UserTable)
            .options(
                joinedload(UserTable.profile).joinedload(UserProfile.podcasts),
                joinedload(UserTable.profile).joinedload(UserProfile.lessons),
            )
            .filter(UserTable.user_id == user_id)
            .first()
        )

        if not user:
            logger.error(
                "No user with associated user_id when retrieving user context??? Manav what did you do?"
            )
            return {"status": "error", "message": "User not found"}
        return user

    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching user data: {str(e)}")
        return {"status": "error", "message": f"An error occurred: {e}"}
