import React from "react";
import { Card } from "../ui/card";
import { Button } from "../ui/button";
import { Slider } from "../ui/slider";
import {
  Play,
  Pause,
  SkipBack,
  SkipForward,
  Volume2,
  ChevronDown,
  ChevronUp,
  Wand2,
} from "lucide-react";

interface AudioPlayerProps {
  title?: string;
  artist?: string;
  currentTime?: number;
  duration?: number;
  isPlaying?: boolean;
  transcript?: string;
  showTranscript?: boolean;
  hasGeneratedAudio?: boolean;
  onGenerateAudio?: () => void;
}

const AudioPlayer = ({
  title = "Understanding Market Basics",
  artist = "Financial Insights Podcast",
  currentTime = 125,
  duration = 360,
  isPlaying = false,
  transcript = "In today's episode, we'll be discussing the fundamental principles of market economics and how they affect your personal investments...",
  showTranscript = false,
  hasGeneratedAudio = false,
  onGenerateAudio = () => {},
}: AudioPlayerProps) => {
  const formatTime = (seconds: number) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    return `${minutes}:${remainingSeconds.toString().padStart(2, "0")}`;
  };

  if (!hasGeneratedAudio) {
    return (
      <Card className="w-full bg-audio-gradient shadow-lg border-b-2 border-primary/20">
        <div className="p-8 flex flex-col items-center justify-center text-center">
          <Wand2 className="h-12 w-12 text-primary mb-4" />
          <h3 className="text-xl font-semibold mb-2 text-card-foreground">
            Generate Audio Summary
          </h3>
          <p className="text-muted-foreground mb-4">
            Get an AI-generated audio summary of your financial insights and
            recent activities
          </p>
          <Button
            onClick={onGenerateAudio}
            size="lg"
            className="bg-primary hover:bg-primary/90"
          >
            Generate Audio
          </Button>
        </div>
      </Card>
    );
  }

  return (
    <Card className="w-full h-auto bg-audio-gradient shadow-lg border-b-2 border-primary/20">
      <div className="p-4">
        <div className="flex items-center justify-between">
          <div className="flex-1">
            <h3 className="font-semibold text-lg text-card-foreground">
              {title}
            </h3>
            <p className="text-sm text-muted-foreground">{artist}</p>
          </div>

          <div className="flex items-center gap-4">
            <Button variant="ghost" size="icon" className="hover:bg-primary/10">
              <SkipBack className="h-5 w-5" />
            </Button>

            <Button
              variant="outline"
              size="icon"
              className="h-10 w-10 border-primary/50 hover:bg-primary/10"
            >
              {isPlaying ? (
                <Pause className="h-5 w-5" />
              ) : (
                <Play className="h-5 w-5" />
              )}
            </Button>

            <Button variant="ghost" size="icon" className="hover:bg-primary/10">
              <SkipForward className="h-5 w-5" />
            </Button>
          </div>

          <div className="flex items-center gap-2 flex-1 justify-end">
            <Volume2 className="h-4 w-4 text-muted-foreground" />
            <div className="w-24">
              <Slider
                defaultValue={[70]}
                max={100}
                step={1}
                className="[&_[role=slider]]:bg-primary [&_[role=slider]]:border-primary"
              />
            </div>
          </div>
        </div>

        <div className="mt-4">
          <div className="relative">
            <Slider
              defaultValue={[(currentTime / duration) * 100]}
              max={100}
              step={1}
              className="[&_[role=slider]]:bg-primary [&_[role=slider]]:border-primary"
            />
            <div className="flex justify-between text-xs text-muted-foreground mt-1">
              <span>{formatTime(currentTime)}</span>
              <span>{formatTime(duration)}</span>
            </div>
          </div>
        </div>

        <div className="mt-2 flex justify-center">
          <Button
            variant="ghost"
            size="sm"
            className="text-xs hover:bg-primary/10"
            onClick={() => {}}
          >
            {showTranscript ? (
              <>
                Hide Transcript
                <ChevronUp className="h-4 w-4 ml-1" />
              </>
            ) : (
              <>
                Show Transcript
                <ChevronDown className="h-4 w-4 ml-1" />
              </>
            )}
          </Button>
        </div>

        {showTranscript && (
          <div className="mt-4 p-4 bg-secondary/50 rounded-md border border-border/50">
            <p className="text-sm text-secondary-foreground">{transcript}</p>
          </div>
        )}
      </div>
    </Card>
  );
};

export default AudioPlayer;
