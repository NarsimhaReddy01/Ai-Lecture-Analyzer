import React, { useState } from "react";
import axios from "axios";

const UploadForm = ({ onUploadComplete }) => {
  const [file, setFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return alert("Please select a video file first!");

    const formData = new FormData();
    formData.append("video", file);

    try {
      setIsUploading(true);
      await axios.post("http://localhost:8000/api/upload/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      alert("✅ Video uploaded successfully!");
      onUploadComplete();
    } catch (err) {
      console.error("Upload failed:", err);
      alert("❌ Upload failed. Check console for details.");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="bg-white shadow-md rounded-lg p-6 mb-6">
      <h2 className="text-lg font-semibold mb-4 text-gray-800">
        🎥 Upload Lecture Video
      </h2>
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <input
          type="file"
          accept="video/mp4,video/x-m4v,video/*"
          onChange={handleFileChange}
          className="border border-gray-300 p-2 rounded-md"
        />
        <button
          type="submit"
          disabled={isUploading}
          className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-md disabled:bg-gray-400"
        >
          {isUploading ? "Uploading..." : "Upload Video"}
        </button>
      </form>
    </div>
  );
};

export default UploadForm;
