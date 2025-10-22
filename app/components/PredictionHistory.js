export default function PredictionHistory({ data }) {
  if (!data.length) return null;

  return (
    <div className="mt-6 overflow-x-auto">
      <h2 className="text-xl font-bold mb-4 text-center">Prediction History</h2>
      <table className="min-w-full border border-gray-200">
        <thead className="bg-gray-100">
          <tr>
            {Object.keys(data[0]).map((key) => (
              <th key={key} className="px-4 py-2 border">{key.replace(/_/g, " ")}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, idx) => (
            <tr key={idx} className="text-center">
              {Object.values(row).map((val, i) => (
                <td key={i} className="px-4 py-2 border">{typeof val === "number" ? val.toFixed(2) : val}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
