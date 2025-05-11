import { useState } from "react";
import ReactMarkdown from "react-markdown";
import "../styles/InsightCard.css";

export default function InsightCard({ markdown }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className={`insight-card ${expanded ? "expanded" : "collapsed"}`}>
      <button className="toggle-btn" onClick={() => setExpanded(!expanded)}>
        {expanded ? "Collapse ▲" : "Expand ▼"}
      </button>
      <div className="insight-content">
        <ReactMarkdown>{markdown}</ReactMarkdown>
      </div>
    </div>
  );
}
