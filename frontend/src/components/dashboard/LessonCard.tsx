import React from "react";
import { Card, CardContent, CardHeader } from "../ui/card";
import { Progress } from "../ui/progress";
import { BookOpen } from "lucide-react";

interface LessonCardProps {
  title?: string;
  description?: string;
  progress?: number;
  imageUrl?: string;
  duration?: string;
}

const LessonCard = ({
  title = "Introduction to Budgeting",
  description = "Learn the fundamentals of creating and maintaining a personal budget",
  progress = 45,
  imageUrl = "https://images.unsplash.com/photo-1554224155-6726b3ff858f?auto=format&fit=crop&q=80",
  duration = "15 mins",
}: LessonCardProps) => {
  return (
    <Card className="w-[320px] bg-card hover:bg-accent transition-colors cursor-pointer h-full">
      <CardHeader className="p-4">
        <div className="relative h-24 w-full rounded-t-lg overflow-hidden">
          <img
            src={imageUrl}
            alt={title}
            className="w-full h-full object-cover"
          />
        </div>
      </CardHeader>
      <CardContent className="p-4 pt-0">
        <h3 className="font-semibold text-lg truncate text-card-foreground">
          {title}
        </h3>
        <p className="text-sm text-muted-foreground line-clamp-2 mb-2">
          {description}
        </p>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <BookOpen className="h-4 w-4" />
            <span>{duration}</span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default LessonCard;
