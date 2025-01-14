import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { ArrowUpIcon, ArrowDownIcon, TrendingUpIcon } from "lucide-react";
import { Progress } from "../ui/progress";

interface AccountCardProps {
  type?: "credit" | "banking" | "retirement" | "brokerage";
  balance?: number;
  trend?: number;
  status?: "positive" | "negative" | "neutral";
  title?: string;
}

const AccountCard = ({
  type = "banking",
  balance = 25000,
  trend = 2.5,
  status = "positive",
  title = "Checking Account",
}: AccountCardProps) => {
  const getStatusColor = () => {
    switch (status) {
      case "positive":
        return "text-green-400";
      case "negative":
        return "text-red-400";
      default:
        return "text-blue-400";
    }
  };

  const getTrendIcon = () => {
    if (trend > 0) return <ArrowUpIcon className="h-4 w-4 text-green-400" />;
    if (trend < 0) return <ArrowDownIcon className="h-4 w-4 text-red-400" />;
    return <TrendingUpIcon className="h-4 w-4 text-blue-400" />;
  };

  return (
    <Card className="bg-card-gradient border-2 border-border hover:bg-accent transition-colors duration-200 shadow-lg">
      <CardHeader className="pb-2">
        <CardTitle className="text-lg font-medium flex items-center justify-between">
          {title}
          <span className={`text-sm ${getStatusColor()}`}>
            {getTrendIcon()}
          </span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div>
            <p className="text-3xl font-bold">${balance.toLocaleString()}</p>
            <p className={`text-sm ${getStatusColor()}`}>
              {trend > 0 ? "+" : ""}
              {trend}% this month
            </p>
          </div>

          {/* Mini trend visualization */}
          <div className="space-y-1.5">
            <Progress value={65} className="h-1" />
            <Progress value={45} className="h-1" />
            <Progress value={85} className="h-1" />
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default AccountCard;
