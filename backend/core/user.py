from pydantic import BaseModel
from pypdf import PdfReader
from data.schema import UserTable, UserProfile
from visibility.logging import logger
from sqlalchemy.exc import SQLAlchemyError


class User(BaseModel):
    """
    A class that represents a user.
    """

    user_id: int | None = None
    username: str | None = None
    password: str | None = None

    async def save_user_to_db(self, db):
        """
        Save the user to the database.
        """
        try:
            new_user = UserTable(username=self.username, password_hash=self.password)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return {
                "status": "success",
                "user_id": new_user.user_id,
                "username": new_user.username,
            }
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"An error occurred while saving user to the database: {e}")
            raise e


class UserFinancialProfile(BaseModel):
    """
    A class that represents a user's financial profile.
    """

    name: str | None = None
    annual_salary: float | None = None
    monthly_takehome: float | None = None
    savings_amount: float | None = None
    retirement_savings: float | None = None
    debt: float | None = None
    dependents: int | None = None
    age: int | None = None
    desired_retirement_age: int | None = None
    state: str | None = None
    financial_goals: list[str] | None = None
    investment_experience: str | None = None
    credit_statement: str | None = None

    async def save_user_profile(self, validated_profile, user_id, db):
        """
        Save the user's financial profile to the database.
        """
        to_save = UserProfile(**validated_profile)
        user = db.query(UserTable).filter(UserTable.user_id == user_id).first()
        if not user:
            logger.error(
                "No user with associated user_id when creating profile??? Manav what did you do?"
            )
        try:
            to_save.user_id = user_id
            db.add(to_save)
            db.commit()
            db.refresh(to_save)
            return {
                "status": "success",
                "profile_id": to_save.profile_id,
                "user_id": to_save.user_id,
            }
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(
                f"An error occurred while saving user profile to the database: {e}"
            )

    def convert_to_prompt_string(self) -> str:
        """
        Convert the user's financial profile to a prompt string.
        """
        prompt_string = f"""
        Name: {self.name}
        Annual Salary: {self.annual_salary}
        Monthly Takehome: {self.monthly_takehome}
        Savings Amount: {self.savings_amount}
        Retirement Savings: {self.retirement_savings}
        Debt: {self.debt}
        Dependents: {self.dependents}
        Age: {self.age}
        Desired Retirement Age: {self.desired_retirement_age}
        State: {self.state}
        Financial Goals: {self.financial_goals}
        Investment Experience: {self.investment_experience}
        Credit Statement: {self.credit_statement}
        """
        return prompt_string

    def parse_statement(pdf_path: str) -> str:
        """
        Parse a credit statement PDF and return the text.
        """
        reader = PdfReader(pdf_path)
        text = reader.get_text()
        return text
