import React, { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

const SignUp: React.FC = () => {
  const [isSignedUp, setIsSignedUp] = useState(false);
  const [formData, setFormData] = useState({
    name: "",
    annual_salary: "",
    monthly_takehome: "",
    savings_amount: "",
    retirement_savings: "",
    debt: "",
    dependents: "",
    age: "",
    desired_retirement_age: "",
    job_title: "",
    company: "",
    education_level: "",
    state: "",
    financial_goals: "",
    investment_experience: ""
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleAuthSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Make sign up API call
    console.log("Sign Up API call");
    setIsSignedUp(true);
  };

  const handleAdditionalFormSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Make additional form API call
    console.log("Additional Form API call", formData);
  };

  return (
    <div>
      {!isSignedUp ? (
        <form className="space-y-6" onSubmit={handleAuthSubmit}>
          <div>
            <label htmlFor="name" className="block text-sm font-medium">
              Username
            </label>
            <Input id="name" name="name" type="text" required />
          </div>
          <div>
            <label htmlFor="password" className="block text-sm font-medium">
              Password
            </label>
            <Input id="password" name="password" type="password" required />
          </div>
          <Button type="submit" className="w-full">
            Sign Up
          </Button>
        </form>
      ) : (
        <form className="space-y-6" onSubmit={handleAdditionalFormSubmit}>
          <div>
            <label htmlFor="annual_salary" className="block text-sm font-medium">
              Annual Salary
            </label>
            <Input id="annual_salary" name="annual_salary" type="number" step="0.01" required onChange={handleInputChange} />
          </div>
          <div>
            <label htmlFor="monthly_takehome" className="block text-sm font-medium">
              Monthly Takehome
            </label>
            <Input id="monthly_takehome" name="monthly_takehome" type="number" step="0.01" required onChange={handleInputChange} />
          </div>
          <div>
            <label htmlFor="savings_amount" className="block text-sm font-medium">
              Savings Amount
            </label>
            <Input id="savings_amount" name="savings_amount" type="number" step="0.01" required onChange={handleInputChange} />
          </div>
          <div>
            <label htmlFor="retirement_savings" className="block text-sm font-medium">
              Retirement Savings
            </label>
            <Input id="retirement_savings" name="retirement_savings" type="number" step="0.01" required onChange={handleInputChange} />
          </div>
          <div>
            <label htmlFor="debt" className="block text-sm font-medium">
              Debt
            </label>
            <Input id="debt" name="debt" type="number" step="0.01" required onChange={handleInputChange} />
          </div>
          <div>
            <label htmlFor="dependents" className="block text-sm font-medium">
              Dependents
            </label>
            <Input id="dependents" name="dependents" type="number" required onChange={handleInputChange} />
          </div>
          <div>
            <label htmlFor="age" className="block text-sm font-medium">
              Age
            </label>
            <Input id="age" name="age" type="number" required onChange={handleInputChange} />
          </div>
          <div>
            <label htmlFor="desired_retirement_age" className="block text-sm font-medium">
              Desired Retirement Age
            </label>
            <Input id="desired_retirement_age" name="desired_retirement_age" type="number" required onChange={handleInputChange} />
          </div>
          <div>
            <label htmlFor="job_title" className="block text-sm font-medium">
              Job Title
            </label>
            <Input id="job_title" name="job_title" type="text" required onChange={handleInputChange} />
          </div>
          <div>
            <label htmlFor="company" className="block text-sm font-medium">
              Company
            </label>
            <Input id="company" name="company" type="text" required onChange={handleInputChange} />
          </div>
          <div>
            <label htmlFor="education_level" className="block text-sm font-medium">
              Education Level
            </label>
            <Input id="education_level" name="education_level" type="text" required onChange={handleInputChange} />
          </div>
          <div>
            <label htmlFor="state" className="block text-sm font-medium">
              State
            </label>
            <Input id="state" name="state" type="text" required onChange={handleInputChange} />
          </div>
          <div>
            <label htmlFor="financial_goals" className="block text-sm font-medium">
              Financial Goals
            </label>
            <Input id="financial_goals" name="financial_goals" type="text" required onChange={handleInputChange} />
          </div>
          <div>
            <label htmlFor="investment_experience" className="block text-sm font-medium">
              Investment Experience
            </label>
            <Input id="investment_experience" name="investment_experience" type="text" required onChange={handleInputChange} />
          </div>
          <Button type="submit" className="w-full">
            Submit
          </Button>
        </form>
      )}
    </div>
  );
};

export default SignUp;