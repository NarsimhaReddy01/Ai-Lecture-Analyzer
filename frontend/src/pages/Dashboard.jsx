import React, { useEffect, useState } from "react";
import { getAllVideos } from "../services/videoService";
import DashboardChart from "../components/DashboardChart";
import ProgressCard from "../components/ProgressCard";

const Dashboard = () => {
  const [videos, setVideos] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getAllVideos().then((data) => {
      setVideos(data);
      setLoading(false);
    });
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950 p-6">
      <h1 className="text-2xl font-bold mb-6 text-center">📊 Student Dashboard</h1>

      {loading ? (
        <p className="text-center text-gray-500">Loading your data...</p>
      ) : (
        <>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-10">
            <ProgressCard title="Total Uploads" value={videos.length} />
            <ProgressCard title="Average Quiz Score" value="82%" />
            <ProgressCard title="Total Study Hours" value="14 hrs" />
          </div>

          <div className="bg-white dark:bg-gray-900 rounded-xl shadow-md p-6">
            <h2 className="text-lg font-semibold mb-4">📈 Progress Overview</h2>
            <DashboardChart />
          </div>

          <div className="mt-10">
            <h2 className="text-lg font-semibold mb-3">🎬 Your Uploaded Lectures</h2>
            <div className="space-y-3">
              {videos.map((v) => (
                <div
                  key={v.id}
                  className="p-4 rounded-lg bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 flex justify-between"
                >
                  <div>
                    <h3 className="font-medium text-gray-800 dark:text-gray-100">{v.title}</h3>
                    <p className="text-sm text-gray-500">{v.language}</p>
                  </div>
                  <button
                    className="text-blue-600 hover:underline"
                    onClick={() => (window.location.href = `/lecture/${v.id}`)}
                  >
                    View →
                  </button>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default Dashboard;
