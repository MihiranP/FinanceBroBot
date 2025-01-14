import React from "react";
import AudioPlayer from "./dashboard/AudioPlayer";
import AccountsGrid from "./dashboard/AccountsGrid";
import AIChatSidebar from "./dashboard/AIChatSidebar";
import EducationSection from "./dashboard/EducationSection";
import StatementsSection from "./dashboard/StatementsSection";

interface HomeProps {
  isAIChatExpanded?: boolean;
  onAIChatToggle?: () => void;
}

const Home = ({
  isAIChatExpanded = true,
  onAIChatToggle = () => {},
}: HomeProps) => {
  const [hasGeneratedAudio, setHasGeneratedAudio] = React.useState(false);

  return (
    <div className="min-h-screen bg-background relative">
      {/* Main Content Area */}
      <div className="p-8 pb-20">
        <div
          className={`transition-all duration-300 ${
            isAIChatExpanded ? "mr-[380px]" : "mr-[50px]"
          }`}
        >
          {/* Main Grid Layout */}
          <div className="space-y-8">
            {/* Audio Player */}
            <section>
              <AudioPlayer
                hasGeneratedAudio={hasGeneratedAudio}
                onGenerateAudio={() => setHasGeneratedAudio(true)}
              />
            </section>

            {/* Accounts Section */}
            <section>
              <AccountsGrid />
            </section>

            {/* Statements Section */}
            <section>
              <StatementsSection />
            </section>

            {/* Education Section */}
            <section>
              <EducationSection />
            </section>
          </div>
        </div>
      </div>

      {/* AI Chat Sidebar */}
      <AIChatSidebar isExpanded={isAIChatExpanded} onToggle={onAIChatToggle} />
    </div>
  );
};

export default Home;
