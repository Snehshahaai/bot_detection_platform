"use client";
import { useState, useEffect } from "react";
import axios from "axios";
import FeatureChart from "../app/components/FeatureChart";
import PredictionForm from "../app/components/PredictionForm";
import PredictionCard from "../app/components/PredictionCard";

export default function Home() {
  const [featureData, setFeatureData] = useState(null);
  const [history, setHistory] = useState([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/feature_importance")
      .then(res => setFeatureData(res.data))
      .catch(err => console.error(err));
  }, []);

  const handleNewPrediction = (prediction) => {
    setHistory([prediction, ...history]); 
  };

  return (
    <div className="max-w-5xl mx-auto mt-10 p-6 font-sans">
      <h1 className="text-4xl font-bold mb-8 text-center text-blue-700">Bot Detection Dashboard</h1>

      <div className="grid md:grid-cols-2 gap-6">
        <PredictionForm onNewPrediction={handleNewPrediction} />
        {featureData && (
          <div className="bg-white p-6 rounded shadow">
            <h2 className="text-xl font-bold mb-4 text-center">Feature Importance</h2>
            <FeatureChart data={featureData} />
          </div>
        )}
      </div>

      <div className="mt-10">
        <h2 className="text-2xl font-bold mb-4 text-center">Recent Predictions</h2>
        {history.length === 0 && <p className="text-center text-gray-500">No predictions yet.</p>}
        {history.map((pred, idx) => (
          <PredictionCard key={idx} prediction={pred} />
        ))}
      </div>
    </div>
  );
}
