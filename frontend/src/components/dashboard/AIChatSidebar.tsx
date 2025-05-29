import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { ScrollArea } from "../ui/scroll-area";
import { Avatar } from "../ui/avatar";
import { SendIcon, ChevronLeftIcon, ChevronRightIcon } from "lucide-react";

interface Message {
  id: number;
  type: "user" | "ai";
  content: string;
  timestamp: string;
}

interface AIChatSidebarProps {
  isExpanded?: boolean;
  messages?: Message[];
  onSend?: (message: string) => void;
  onToggle?: () => void;
}

const AIChatSidebar = ({
  isExpanded = true,
  messages = [
    {
      id: 1,
      type: "ai",
      content: "Hello! How can I help you with your finances today?",
      timestamp: "9:00 AM",
    },
    {
      id: 2,
      type: "user",
      content: "What are some tips for budgeting?",
      timestamp: "9:01 AM",
    },
    {
      id: 3,
      type: "ai",
      content:
        "I can help you create a budget! First, let's track your monthly income and expenses...",
      timestamp: "9:01 AM",
    },
  ],
  onSend = () => {},
  onToggle = () => {},
}: AIChatSidebarProps) => {
  const [inputValue, setInputValue] = React.useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim()) {
      onSend(inputValue);
      setInputValue("");
    }
  };

  return (
    <div
      className={`fixed right-0 top-0 h-screen bg-sidebar-gradient transition-all duration-300 shadow-lg flex border-l border-border ${isExpanded ? "w-[380px]" : "w-[50px]"}`}
    >
      <button
        onClick={onToggle}
        className="absolute left-0 top-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-primary rounded-full p-2 shadow-md hover:bg-primary/80"
      >
        {!isExpanded ? (
          <ChevronRightIcon size={20} className="text-card-foreground" />
        ) : (
          <ChevronLeftIcon size={20} className="text-card-foreground" />
        )}
      </button>

      {isExpanded && (
        <Card className="w-full h-full border-0 rounded-none bg-transparent">
          <CardHeader className="border-b border-border">
            <CardTitle className="text-xl text-card-foreground">
              Financial Assistant
            </CardTitle>
          </CardHeader>
          <CardContent className="p-4 h-[calc(100%-160px)]">
            <ScrollArea className="h-full pr-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex gap-3 mb-4 ${message.type === "user" ? "flex-row-reverse" : ""}`}
                >
                  <Avatar className="h-8 w-8">
                    <img
                      src={
                        message.type === "ai"
                          ? "https://api.dicebear.com/7.x/bottts/svg?seed=fin-ai"
                          : "https://api.dicebear.com/7.x/avataaars/svg?seed=user"
                      }
                      alt={message.type === "ai" ? "AI" : "User"}
                    />
                  </Avatar>
                  <div
                    className={`rounded-lg p-3 max-w-[80%] ${message.type === "user" ? "bg-primary text-primary-foreground" : "bg-secondary text-secondary-foreground"}`}
                  >
                    <p className="text-sm">{message.content}</p>
                    <span className="text-xs opacity-50 mt-1 block">
                      {message.timestamp}
                    </span>
                  </div>
                </div>
              ))}
            </ScrollArea>
          </CardContent>
          <div className="absolute bottom-0 left-0 right-0 p-4 bg-card border-t border-border">
            <form onSubmit={handleSubmit} className="flex gap-2">
              <Input
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Ask me about your finances..."
                className="flex-1 bg-secondary text-secondary-foreground"
              />
              <Button type="submit" size="icon">
                <SendIcon className="h-4 w-4" />
              </Button>
            </form>
          </div>
        </Card>
      )}
    </div>
  );
};

export default AIChatSidebar;
