import ReactMarkdown from "react-markdown";
import "../styles/InsightCard.css";

//import rehypeHighlight from "rehype-highlight";

export default function InsightCard({ markdown }) {
  // Set expanded to true by default and remove the toggle functionality

  // Strip code fence markers if present
  const cleanMarkdown = markdown.replace(/```markdown|```/g, "").trim();

  // Define custom renderers for markdown elements
  const components = {
    // Center h1 headings and ensure proper positioning
    h1: ({ node, children, ...props }) => (
      <h1 className="insight-heading insight-h1" {...props}>
        {children}
      </h1>
    ),
    h2: ({ node, children, ...props }) => (
      <h2 className="insight-heading" {...props}>
        {children}
      </h2>
    ),
    h3: ({ node, children, ...props }) => (
      <h3 className="insight-heading" {...props}>
        {children}
      </h3>
    ),
    h4: ({ node, children, ...props }) => (
      <h4 className="insight-heading" {...props}>
        {children}
      </h4>
    ),
    h5: ({ node, children, ...props }) => (
      <h5 className="insight-heading" {...props}>
        {children}
      </h5>
    ),
    h6: ({ node, children, ...props }) => (
      <h6 className="insight-heading" {...props}>
        {children}
      </h6>
    ),

    // Italicize list items
    li: ({ node, ...props }) => <li className="insight-list-item" {...props} />,

    // Bold text styling (already handled by default, but we can enhance)
    strong: ({ node, ...props }) => (
      <strong className="insight-bold" {...props} />
    ),
  };

  return (
    <div className="insight-card expanded">
      <div className="insight-content">
        <ReactMarkdown >
          {cleanMarkdown}
        </ReactMarkdown>
      </div>
    </div>
  );
}
