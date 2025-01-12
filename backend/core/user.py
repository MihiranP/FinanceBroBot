from pydantic import BaseModel


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
