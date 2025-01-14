import React from "react";
import AccountCard from "./AccountCard";
import { Card, CardContent } from "../ui/card";
import { Avatar } from "../ui/avatar";
import { Briefcase, GraduationCap, MapPin, Target, Users } from "lucide-react";

interface ProfileData {
  name?: string;
  annual_salary?: number;
  monthly_takehome?: number;
  savings_amount?: number;
  retirement_savings?: number;
  debt?: number;
  dependents?: number;
  age?: number;
  desired_retirement_age?: number;
  job_title?: string;
  company?: string;
  education_level?: string;
  state?: string;
  financial_goals?: string[];
  investment_experience?: string;
}

interface AccountsGridProps {
  profileData?: ProfileData;
}

const AccountsGrid = ({
  profileData = {
    name: "John Doe",
    annual_salary: 85000,
    monthly_takehome: 5200,
    savings_amount: 25000,
    retirement_savings: 150000,
    debt: 35000,
    dependents: 2,
    age: 32,
    desired_retirement_age: 65,
    job_title: "Software Engineer",
    company: "Tech Corp",
    education_level: "Bachelor's Degree",
    state: "California",
    financial_goals: ["Buy a house", "Save for retirement"],
    investment_experience: "Intermediate",
  },
}: AccountsGridProps) => {
  const accounts = [
    {
      type: "banking",
      balance: profileData.savings_amount || 0,
      trend: 2.5,
      status: "positive",
      title: "Savings",
    },
    {
      type: "retirement",
      balance: profileData.retirement_savings || 0,
      trend: 5.8,
      status: "positive",
      title: "Retirement",
    },
    {
      type: "credit",
      balance: profileData.debt || 0,
      trend: -1.2,
      status: "negative",
      title: "Total Debt",
    },
    {
      type: "banking",
      balance: profileData.monthly_takehome || 0,
      trend: 0,
      status: "neutral",
      title: "Monthly Income",
    },
  ];

  return (
    <div className="w-full space-y-8">
      {/* Profile Overview */}
      <Card className="p-8 bg-card">
        <CardContent className="p-0 flex items-start gap-8">
          <Avatar className="h-20 w-20">
            <img
              src={`https://api.dicebear.com/7.x/avataaars/svg?seed=${profileData.name}`}
              alt={profileData.name}
            />
          </Avatar>

          <div className="flex-1 space-y-6">
            <div>
              <h2 className="text-3xl font-semibold">{profileData.name}</h2>
              <div className="flex gap-6 text-sm text-muted-foreground mt-2">
                <span className="flex items-center gap-2">
                  <Briefcase className="h-4 w-4" />
                  {profileData.job_title} at {profileData.company}
                </span>
                <span className="flex items-center gap-2">
                  <GraduationCap className="h-4 w-4" />
                  {profileData.education_level}
                </span>
                <span className="flex items-center gap-2">
                  <MapPin className="h-4 w-4" />
                  {profileData.state}
                </span>
              </div>
            </div>

            <div className="flex gap-8 text-sm">
              <div className="flex items-center gap-2">
                <Users className="h-4 w-4 text-muted-foreground" />
                <span>Age: {profileData.age}</span>
                <span className="mx-2">•</span>
                <span>Dependents: {profileData.dependents}</span>
              </div>
              <div className="flex items-center gap-2">
                <Target className="h-4 w-4 text-muted-foreground" />
                <span>
                  Target Retirement: {profileData.desired_retirement_age}
                </span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Financial Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        {accounts.map((account, index) => (
          <AccountCard
            key={index}
            type={account.type}
            balance={account.balance}
            trend={account.trend}
            status={account.status}
            title={account.title}
          />
        ))}
      </div>
    </div>
  );
};

export default AccountsGrid;
