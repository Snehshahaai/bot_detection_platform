import { useState } from "react";
import axios from "axios";

export default function PredictionForm({ onNewPrediction }) {
  const [formData, setFormData] = useState({
    followers_count: "",
    following_count: "",
    post_count: "",
    account_age_days: "",
    has_profile_picture: 1,
    has_bio: 1,
    avg_post_interval: "",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://127.0.0.1:8000/predict", {
        ...formData,
        followers_count: Number(formData.followers_count),
        following_count: Number(formData.following_count),
        post_count: Number(formData.post_count),
        account_age_days: Number(formData.account_age_days),
        has_profile_picture: Number(formData.has_profile_picture),
        has_bio: Number(formData.has_bio),
        avg_post_interval: Number(formData.avg_post_interval),
      });
      onNewPrediction({ ...formData, ...response.data });
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 bg-white p-6 rounded shadow">
      {Object.keys(formData).map((key) => (
        <div key={key}>
          <label className="block font-semibold mb-1">{key.replace(/_/g, " ")}</label>
          <input
            type="number"
            name={key}
            value={formData[key]}
            onChange={handleChange}
            step="any"
            className="w-full p-2 border border-gray-300 rounded"
            required
          />
        </div>
      ))}
      <button className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">Predict</button>
    </form>
  );
}
