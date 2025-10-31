import React, { useState } from "react";
import { generatePresignedUrl, uploadToS3 } from "../services/videoService";

const UploadPage = () => {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");

  const handleUpload = async () => {
    if (!file) return alert("Please choose a file first!");

    try {
      setStatus("Generating upload link...");
      const presignedData = await generatePresignedUrl(file.name, file.type);

      setStatus("Uploading to S3...");
      const fileUrl = await uploadToS3(presignedData, file);

      setStatus(`✅ Upload successful! File URL: ${fileUrl}`);
    } catch (error) {
      console.error("Upload failed:", error);
      setStatus("❌ Upload failed. Check console for details.");
    }
  };

  return (
    <div className="p-6 bg-white shadow-md rounded-md max-w-md mx-auto">
      <h2 className="text-lg font-semibold mb-4">Upload Lecture Video</h2>
      <input
        type="file"
        accept="video/*"
        onChange={(e) => setFile(e.target.files[0])}
        className="mb-4"
      />
      <button
        onClick={handleUpload}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Upload
      </button>
      <p className="mt-4 text-gray-700">{status}</p>
    </div>
  );
};

export default UploadPage;
