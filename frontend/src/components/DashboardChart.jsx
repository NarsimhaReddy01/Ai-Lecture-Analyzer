import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

/**
 * DashboardChart — displays user performance trends over time.
 * Props:
 *   - data: Array of { date, score }
 */
const DashboardChart = ({ data }) => {
  if (!data || data.length === 0) {
    return (
      <div className="text-gray-500 text-center py-6">
        📈 No performance data yet. Complete a few quizzes to see progress!
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h3 className="text-lg font-semibold mb-4 text-blue-700">
        📊 Quiz Performance Over Time
      </h3>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" stroke="#555" />
          <YAxis domain={[0, 100]} stroke="#555" />
          <Tooltip />
          <Legend />
          <Line
            type="monotone"
            dataKey="score"
            stroke="#3b82f6"
            activeDot={{ r: 8 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default DashboardChart;
