export default function PredictionCard({ prediction }) {
  const isBot = prediction.prediction === 1;
  const cardColor = isBot ? "bg-red-100 border-red-400" : "bg-green-100 border-green-400";
  const textColor = isBot ? "text-red-700" : "text-green-700";

  return (
    <div
      className={`p-4 border-l-8 rounded shadow mb-4 transition transform hover:scale-105 ${cardColor}`}
    >
      <h3 className={`text-lg font-bold mb-2 ${textColor}`}>
        {isBot ? "Bot Detected 🤖" : "Human ✅"} — Probability: {(prediction.probability * 100).toFixed(2)}%
      </h3>
      <div className="grid grid-cols-2 gap-2 text-sm">
        {Object.entries(prediction).map(([key, value]) => {
          if (key === "prediction" || key === "probability") return null;
          return (
            <div key={key}>
              <span className="font-semibold">{key.replace(/_/g, " ")}:</span> {value}
            </div>
          );
        })}
      </div>
    </div>
  );
}
