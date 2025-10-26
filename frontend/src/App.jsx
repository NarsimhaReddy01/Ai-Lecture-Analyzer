// frontend/src/App.jsx
import React, { useEffect, useState } from "react";
import axios from "axios";

const API_BASE = "http://127.0.0.1:8000/api/videos/";

function App() {
  const [videos, setVideos] = useState([]);
  const [selectedVideo, setSelectedVideo] = useState(null);
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  const fetchVideos = async () => {
    try {
      const response = await axios.get(`${API_BASE}list/`);
      setVideos(response.data);
    } catch (error) {
      console.error("Error fetching videos", error);
    }
  };

  useEffect(() => {
    fetchVideos();
  }, []);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return alert("Please select a video first!");

    setUploading(true);
    try {
      const res = await axios.post(`${API_BASE}upload-url/`, {
        file_name: file.name,
        file_type: file.type,
      });

      const { data, file_url, video_id } = res.data;
      await axios.post(data.url, file, { headers: { "Content-Type": file.type } });

      alert("Video uploaded successfully! Processing started.");
      fetchVideos();
    } catch (error) {
      console.error("Upload failed:", error);
      alert("Upload failed. Please try again.");
    }
    setUploading(false);
  };

  const handleVideoSelect = async (videoId) => {
    try {
      const res = await axios.get(`${API_BASE}${videoId}/status/`);
      setSelectedVideo(res.data);
    } catch (error) {
      console.error("Error fetching video status", error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 text-gray-800 p-8">
      <h1 className="text-3xl font-bold mb-4">🎥 Lecture Video Analyzer</h1>

      {/* Upload Section */}
      <div className="bg-white p-4 rounded-xl shadow mb-6">
        <h2 className="text-xl font-semibold mb-2">Upload a New Video</h2>
        <input type="file" onChange={handleFileChange} className="mb-2" />
        <button
          onClick={handleUpload}
          disabled={uploading}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-400"
        >
          {uploading ? "Uploading..." : "Upload"}
        </button>
      </div>

      {/* Videos List */}
      <div className="bg-white p-4 rounded-xl shadow mb-6">
        <h2 className="text-xl font-semibold mb-2">Your Uploaded Videos</h2>
        {videos.length === 0 ? (
          <p>No videos uploaded yet.</p>
        ) : (
          <ul className="space-y-2">
            {videos.map((video) => (
              <li
                key={video.video_id}
                className="p-2 border rounded cursor-pointer hover:bg-gray-50 flex justify-between"
                onClick={() => handleVideoSelect(video.video_id)}
              >
                <span>{video.title}</span>
                <span
                  className={`text-sm px-2 py-1 rounded ${
                    video.status === "done"
                      ? "bg-green-100 text-green-700"
                      : "bg-yellow-100 text-yellow-700"
                  }`}
                >
                  {video.status}
                </span>
              </li>
            ))}
          </ul>
        )}
      </div>

      {/* Video Details */}
      {selectedVideo && (
        <div className="bg-white p-4 rounded-xl shadow">
          <h2 className="text-xl font-semibold mb-2">{selectedVideo.title}</h2>
          <p className="text-gray-600 mb-2">
            Status:{" "}
            <strong
              className={
                selectedVideo.status === "done"
                  ? "text-green-600"
                  : "text-yellow-600"
              }
            >
              {selectedVideo.status}
            </strong>
          </p>

          {selectedVideo.transcript && (
            <>
              <h3 className="font-semibold mt-3">Transcript:</h3>
              <p className="text-sm bg-gray-50 p-2 rounded">
                {selectedVideo.transcript}
              </p>
            </>
          )}

          {selectedVideo.summary && (
            <>
              <h3 className="font-semibold mt-3">Summary:</h3>
              <p className="text-sm bg-gray-50 p-2 rounded">
                {selectedVideo.summary}
              </p>
            </>
          )}

          {selectedVideo.quiz_questions && selectedVideo.quiz_questions.length > 0 && (
            <>
              <h3 className="font-semibold mt-3">Quiz Questions:</h3>
              <ul className="list-disc ml-5">
                {selectedVideo.quiz_questions.map((q, idx) => (
                  <li key={idx}>{q.question}</li>
                ))}
              </ul>
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
