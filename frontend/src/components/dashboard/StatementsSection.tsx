import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { Button } from "../ui/button";
import { FileText, Download, Calendar } from "lucide-react";
import { ScrollArea } from "../ui/scroll-area";

interface Statement {
  id: string;
  type: "bank" | "credit";
  name: string;
  date: string;
  fileUrl: string;
}

interface StatementsSectionProps {
  statements?: Statement[];
}

const StatementsSection = ({
  statements = [
    {
      id: "1",
      type: "bank",
      name: "Checking Account Statement",
      date: "January 2024",
      fileUrl: "#",
    },
    {
      id: "2",
      type: "credit",
      name: "Credit Card Statement",
      date: "January 2024",
      fileUrl: "#",
    },
    {
      id: "3",
      type: "bank",
      name: "Savings Account Statement",
      date: "January 2024",
      fileUrl: "#",
    },
  ],
}: StatementsSectionProps) => {
  return (
    <Card className="w-full bg-card-gradient border-2 border-border shadow-lg">
      <CardHeader>
        <CardTitle className="text-xl font-semibold flex items-center gap-2 text-card-foreground">
          <FileText className="h-5 w-5" />
          Statements
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-[300px] pr-4">
          <div className="space-y-4">
            {statements.map((statement) => (
              <div
                key={statement.id}
                className="flex items-center justify-between p-4 rounded-lg border border-border/50 hover:bg-accent/50 transition-colors"
              >
                <div className="flex items-start gap-3">
                  <FileText className="h-5 w-5 text-primary mt-1" />
                  <div>
                    <h4 className="font-medium text-card-foreground">
                      {statement.name}
                    </h4>
                    <div className="flex items-center gap-2 text-sm text-muted-foreground">
                      <Calendar className="h-4 w-4" />
                      {statement.date}
                    </div>
                  </div>
                </div>
                <Button variant="ghost" size="icon">
                  <Download className="h-4 w-4" />
                </Button>
              </div>
            ))}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  );
};

export default StatementsSection;
