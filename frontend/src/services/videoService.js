/**
 * 🎥 Video Service - Handles all API interactions for lecture videos
 */

import { API } from "./api";

/**
 * 1️⃣ Get all uploaded videos
 */
export const getAllVideos = async () => {
  const res = await API.get("/videos/");
  return res.data;
};

/**
 * 2️⃣ Get details for a specific video
 */
export const getVideoDetails = async (videoId) => {
  const res = await API.get(`/videos/${videoId}/`);
  return res.data;
};

/**
 * 3️⃣ Generate AWS S3 presigned URL (backend creates DB entry + returns upload fields)
 */
export const generatePresignedUrl = async (fileName, fileType) => {
  const res = await API.post("/videos/upload/", {
    file_name: fileName,
    file_type: fileType,
  });
  return res.data;
};

/**
 * 4️⃣ Upload file directly to S3 using the presigned POST data
 */
export const uploadToS3 = async (presignedData, file) => {
  const formData = new FormData();

  Object.entries(presignedData.data.fields).forEach(([key, value]) => {
    formData.append(key, value);
  });

  formData.append("file", file);

  const response = await fetch(presignedData.data.url, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("❌ S3 upload failed");
  }

  return presignedData.file_url;
};

/**
 * 5️⃣ Check video processing status (Celery task progress)
 */
export const getVideoStatus = async (videoId) => {
  const res = await API.get(`/videos/${videoId}/status/`);
  return res.data;
};

/**
 * 6️⃣ Delete a video (Admin only)
 */
export const deleteVideo = async (videoId) => {
  const res = await API.delete(`/videos/${videoId}/`);
  return res.data;
};
