import ReactMarkdown from "react-markdown";
import "../styles/InsightPane.css";

export default function InsightPane({ markdown }) {
    return (
      <div className="insight-pane">
        <ReactMarkdown>{markdown}</ReactMarkdown>
        
      </div>
    );
  }
  