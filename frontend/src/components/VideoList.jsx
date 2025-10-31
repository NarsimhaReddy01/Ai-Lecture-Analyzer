import React, { useEffect, useState } from "react";
import axios from "axios";

const VideoList = ({ onSelectVideo }) => {
  const [videos, setVideos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    const fetchVideos = async () => {
      try {
        const res = await axios.get("http://localhost:8000/api/videos/");
        setVideos(res.data);
      } catch (err) {
        console.error(err);
        setError("Failed to load videos.");
      } finally {
        setLoading(false);
      }
    };
    fetchVideos();
  }, []);

  if (loading) return <div>Loading videos...</div>;
  if (error) return <div className="text-red-600">{error}</div>;
  if (videos.length === 0)
    return <div className="text-gray-500">No videos uploaded yet.</div>;

  return (
    <div className="bg-white shadow-md rounded-lg p-4 max-h-[500px] overflow-y-auto">
      <h2 className="text-lg font-semibold mb-3 text-gray-800">
        📁 Uploaded Videos
      </h2>
      <ul className="space-y-2">
        {videos.map((video) => (
          <li
            key={video.id}
            onClick={() => {
              setSelected(video.id);
              onSelectVideo(video.id);
            }}
            className={`p-3 rounded-md cursor-pointer border ${
              selected === video.id
                ? "bg-blue-100 border-blue-500"
                : "bg-gray-50 hover:bg-gray-100 border-gray-300"
            }`}
          >
            🎥 {video.title || "Untitled Video"}
            <div className="text-xs text-gray-500 mt-1">
              Uploaded: {new Date(video.created_at).toLocaleString()}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default VideoList;
