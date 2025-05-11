import { useState } from "react";
import Dashboard from "./Dashboard";
import InsightCard from "./InsightCard";
import "../styles/DashboardTabs.css";

export default function DashboardTabs({ charts, insights_md }) {
  const [activeTab, setActiveTab] = useState("charts");

  return (
    <div className="dashboard-tabs">
      <div className="tab-header">
        <button
          className={activeTab === "charts" ? "active" : ""}
          onClick={() => setActiveTab("charts")}
        >
          📊 Charts
        </button>
        <button
          className={activeTab === "insights" ? "active" : ""}
          onClick={() => setActiveTab("insights")}
        >
          🧠 Insights
        </button>
      </div>

      <div className="tab-content">
        {activeTab === "charts" && <Dashboard charts={charts} />}
        {activeTab === "insights" && <InsightCard markdown={insights_md} />}
      </div>
    </div>
  );
}

