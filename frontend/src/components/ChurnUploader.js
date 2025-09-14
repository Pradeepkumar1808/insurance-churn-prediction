// src/components/ChurnUploader.js
import React, { useState } from "react";
import axios from "axios";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const ChurnUploader = () => {
  const [file, setFile] = useState(null);
  const [predictions, setPredictions] = useState([]);
  const [chartData, setChartData] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return alert("Please select a CSV file first.");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://127.0.0.1:8000/predict", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      const data = response.data.predictions;
      setPredictions(data);

      // Count churn vs non-churn
      const churnCount = data.filter((row) => row.churn_pred === 1).length;
      const nonChurnCount = data.filter((row) => row.churn_pred === 0).length;

      setChartData({
        labels: ["Non-Churn", "Churn"],
        datasets: [
          {
            label: "Number of Customers",
            data: [nonChurnCount, churnCount],
            backgroundColor: ["#4caf50", "#f44336"],
          },
        ],
      });
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("Failed to get predictions.");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Insurance Churn Prediction</h2>
      <input type="file" accept=".csv" onChange={handleFileChange} />
      <button onClick={handleUpload} style={{ marginLeft: "10px" }}>
        Upload & Predict
      </button>

      {predictions.length > 0 && (
        <div style={{ marginTop: "30px" }}>
          <h3>Predictions Table</h3>
          <table border="1" cellPadding="5" style={{ borderCollapse: "collapse" }}>
            <thead>
              <tr>
                {Object.keys(predictions[0]).map((col) => (
                  <th key={col}>{col}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {predictions.map((row, idx) => (
                <tr key={idx}>
                  {Object.values(row).map((val, i) => (
                    <td key={i}>{val}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>

          {chartData && (
            <div style={{ maxWidth: "500px", marginTop: "30px" }}>
              <h3>Churn Visualization</h3>
              <Bar data={chartData} />
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ChurnUploader;
