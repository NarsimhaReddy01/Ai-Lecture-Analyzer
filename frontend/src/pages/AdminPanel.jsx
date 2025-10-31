import React, { useEffect, useState } from "react";
import { getAllVideos } from "../services/videoService";
import { API } from "../services/api";

const AdminPanel = () => {
  const [videos, setVideos] = useState([]);
  const [apiKey, setApiKey] = useState("");
  const [message, setMessage] = useState("");

  useEffect(() => {
    getAllVideos().then(setVideos);
  }, []);

  const updateApiKey = async () => {
    try {
      await API.post("/admin/update-key/", { api_key: apiKey });
      setMessage("✅ API key updated successfully!");
    } catch {
      setMessage("❌ Failed to update API key.");
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950 p-6">
      <h1 className="text-2xl font-bold mb-6 text-center">🧑‍🏫 Admin Panel</h1>

      <div className="bg-white dark:bg-gray-900 rounded-xl shadow-md p-6 mb-8">
        <h2 className="text-lg font-semibold mb-3">🔑 Update API Key</h2>
        <input
          type="text"
          placeholder="Enter new API key"
          value={apiKey}
          onChange={(e) => setApiKey(e.target.value)}
          className="w-full p-2 border border-gray-300 dark:border-gray-700 rounded mb-3"
        />
        <button
          onClick={updateApiKey}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Update Key
        </button>
        {message && <p className="mt-2 text-gray-600 dark:text-gray-400">{message}</p>}
      </div>

      <div className="bg-white dark:bg-gray-900 rounded-xl shadow-md p-6">
        <h2 className="text-lg font-semibold mb-4">🎞 Uploaded Videos</h2>
        {videos.map((v) => (
          <div
            key={v.id}
            className="border-b border-gray-200 dark:border-gray-700 py-3 flex justify-between"
          >
            <div>
              <p className="font-medium">{v.title}</p>
              <p className="text-sm text-gray-500">{v.language}</p>
            </div>
            <div className="flex gap-3">
              <a
                href={v.transcript_url}
                className="text-blue-600 hover:underline"
                target="_blank"
                rel="noreferrer"
              >
                Transcript
              </a>
              <a
                href={v.summary_url}
                className="text-green-600 hover:underline"
                target="_blank"
                rel="noreferrer"
              >
                Summary
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AdminPanel;
