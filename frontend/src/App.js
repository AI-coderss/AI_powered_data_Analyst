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
  const [isChatLoading, setIsChatLoading] = useState(false);

  const handleUpload = async (file) => {
    setIsLoading(true);
    setDashSpec(null);
    setChatInsights("");

    const form = new FormData();
    form.append("file", file);

    try {
      const res = await fetch("http://127.0.0.1:5050/upload", {
        method: "POST",
        body: form,
      });

      const result = await res.json();
      setDashSpec(result);

      setTimeout(() => {
        document
          .getElementById("dashboard")
          ?.scrollIntoView({ behavior: "smooth" });
      }, 300);
    } catch (err) {
      console.error("Upload failed:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleChatPrompt = async (prompt) => {
    setIsChatLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:5050/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt, data: dashSpec?.data }),
      });

      const data = await res.json();
      console.log("data type", data.type);
      console.log("data content", data.content);
      console.log("data reply", data.reply);
      console.log("data", data);

      if (data.type === "insights") {
        setChatInsights(data.reply);
      } else if (data.type === "charts") {
        setDashSpec((prevDashSpec) => ({
          ...prevDashSpec,
          charts: data.reply,
        }));
      }
    } catch (err) {
      console.error("Chat request failed:", err);
    } finally {
      setIsChatLoading(false);
    }
  };

  return (
    <div className="app-root">
      <Title />

      <main className="app-main">
        <aside className="sidebar">
          <Sidebar />
        </aside>

        <section className="content" id="dashboard">
          {isLoading || isChatLoading ? (
            <Loader isLoading={true} />
          ) : (
            dashSpec && (
              <DashboardTabs
                charts={dashSpec.charts}
                insights_md={chatInsights || dashSpec.insights}
              />
            )
          )}
        </section>
      </main>

      <div className="bottom-bar">
        <div className="chat-wrapper">
          <ChatInputWidget
            onSendMessage={handleChatPrompt}
            disabled={isChatLoading}
          />
        </div>
        <div className="uploader-wrapper">
          <Uploader
            onFile={handleUpload}
            disabled={isLoading || isChatLoading}
          />
        </div>
      </div>
    </div>
  );
}
