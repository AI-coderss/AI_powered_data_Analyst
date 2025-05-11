import React, { useState } from "react";
import Uploader from "./components/Uploader";
import ChatInputWidget from "./components/ChatInputWidget";
import Sidebar from "./components/Sidebar";
import Loader from "./components/Loader";
import Title from "./components/Title";
import DashboardTabs from "./components/DashboardTabs"; // ✅ new tabbed component

import "./styles/Uploader.css";
import "./styles/Dashboard.css";
import "./styles/InsightPane.css";
import "./styles/app.css";
import "./styles/Loader.css";
import "./styles/DashboardTabs.css"; // ✅ tab styles

export default function App() {
  const [dashSpec, setDashSpec] = useState(null);
  const [chatInsights, setChatInsights] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleUpload = async (file) => {
    setIsLoading(true);
    setDashSpec(null);
    setChatInsights("");

    const form = new FormData();
    form.append("file", file);

    try {
      const res = await fetch("https://ai-powered-data-analyst-backend.onrender.com/upload", {
        method: "POST",
        body: form,
      });

      const result = await res.json();
      setDashSpec(result);

      setTimeout(() => {
        document.getElementById("dashboard")?.scrollIntoView({ behavior: "smooth" });
      }, 300);
    } catch (err) {
      console.error("Upload failed:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleChatPrompt = async (prompt) => {
    const res = await fetch("https://ai-powered-data-analyst-backend.onrender.com/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt, data: dashSpec?.data }),
    });

    const data = await res.json();
    setChatInsights(data.response);
  };

  return (
    <div className="app-root">
      <Title />

      <main className="app-main">
        <aside className="sidebar">
          <Sidebar />
        </aside>

        <section className="content" id="dashboard">
          {isLoading ? (
            <Loader isLoading={true} />
          ) : (
            dashSpec && (
              <DashboardTabs
                charts={dashSpec.charts}
                insights_md={chatInsights || dashSpec.insights_md}
              />
            )
          )}
        </section>
      </main>

      <div className="bottom-bar">
        <div className="chat-wrapper">
          <ChatInputWidget onSendMessage={handleChatPrompt} />
        </div>
        <div className="uploader-wrapper">
          <Uploader onFile={handleUpload} />
        </div>
      </div>
    </div>
  );
}






