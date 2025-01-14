import React from "react";
import { ScrollArea } from "../ui/scroll-area";
import { Button } from "../ui/button";
import { ChevronLeft, ChevronRight } from "lucide-react";
import LessonCard from "./LessonCard";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";

interface EducationSectionProps {
  lessons?: Array<{
    id: string;
    title: string;
    description: string;
    progress: number;
    imageUrl: string;
    duration: string;
  }>;
}

const EducationSection = ({
  lessons = [
    {
      id: "1",
      title: "Introduction to Budgeting",
      description:
        "Learn the fundamentals of creating and maintaining a personal budget",
      progress: 45,
      imageUrl: "https://images.unsplash.com/photo-1554224155-6726b3ff858f",
      duration: "15 mins",
    },
    {
      id: "2",
      title: "Investment Basics",
      description: "Understanding stocks, bonds, and mutual funds",
      progress: 30,
      imageUrl: "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f",
      duration: "20 mins",
    },
    {
      id: "3",
      title: "Debt Management",
      description: "Strategies for managing and reducing debt effectively",
      progress: 60,
      imageUrl: "https://images.unsplash.com/photo-1579621970563-ebec7560ff3e",
      duration: "25 mins",
    },
    {
      id: "4",
      title: "Retirement Planning",
      description: "Planning for a secure financial future",
      progress: 15,
      imageUrl: "https://images.unsplash.com/photo-1532619675605-1ede6c2ed2b0",
      duration: "30 mins",
    },
  ],
}: EducationSectionProps) => {
  const scrollContainerRef = React.useRef<HTMLDivElement>(null);

  const scroll = (direction: "left" | "right") => {
    if (scrollContainerRef.current) {
      const scrollAmount = 340; // card width + gap
      const scrollLeft = scrollContainerRef.current.scrollLeft;
      const newScrollLeft =
        direction === "left"
          ? scrollLeft - scrollAmount
          : scrollLeft + scrollAmount;

      scrollContainerRef.current.scrollTo({
        left: newScrollLeft,
        behavior: "smooth",
      });
    }
  };

  return (
    <Card className="w-full bg-card-gradient p-6 min-h-[300px]">
      <CardHeader className="px-0 pt-0">
        <div className="flex justify-between items-center">
          <CardTitle className="text-2xl font-bold text-card-foreground">
            Financial Education
          </CardTitle>
          <div className="flex gap-2">
            <Button
              variant="outline"
              size="icon"
              onClick={() => scroll("left")}
            >
              <ChevronLeft className="h-4 w-4" />
            </Button>
            <Button
              variant="outline"
              size="icon"
              onClick={() => scroll("right")}
            >
              <ChevronRight className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </CardHeader>

      <CardContent className="px-0">
        <ScrollArea className="w-full" ref={scrollContainerRef}>
          <div className="flex gap-5 pb-4">
            {lessons.map((lesson) => (
              <LessonCard
                key={lesson.id}
                title={lesson.title}
                description={lesson.description}
                progress={lesson.progress}
                imageUrl={lesson.imageUrl}
                duration={lesson.duration}
              />
            ))}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  );
};

export default EducationSection;
