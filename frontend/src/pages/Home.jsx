// pages/Home.js
import React, { useState } from "react";
import Dashboard from "../components/Dashboard";
import "../styles/Dashboard.css";

const Home = () => {
  const [data, setData] = useState([]);
  const [insights, setInsights] = useState("");

  const handleUpload = async (e) => {
    const formData = new FormData();
    formData.append("file", e.target.files[0]);

    const res = await fetch("http://localhost:5000/upload", {
      method: "POST",
      body: formData,
    });

    const result = await res.json();
    setData(result.data);
    setInsights(result.insights);
  };

  return (
    <div className="dashboard-container">
      <div className="file-upload">
        <h2>Upload Data File</h2>
        <input type="file" onChange={handleUpload} />
      </div>
      {data.length > 0 && <Dashboard data={data} />}
      {insights && (
        <div className="chart-wrapper" style={{ marginTop: "20px" }}>
          <h3>AI Insights</h3>
          <p>{insights}</p>
        </div>
      )}
    </div>
  );
};

export default Home;
