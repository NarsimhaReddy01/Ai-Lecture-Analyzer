import React, { useState, useEffect } from "react";
import axios from "axios";

const UploadVideo = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [videoId, setVideoId] = useState(null);
  const [status, setStatus] = useState("");
  const [transcript, setTranscript] = useState("");
  const [summary, setSummary] = useState("");
  const [quiz, setQuiz] = useState([]);

  // --- Handle file selection ---
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  // --- Upload file to S3 via presigned URL ---
  const handleUpload = async () => {
    if (!file) return alert("Select a video first!");
    setUploading(true);

    try {
      // 1. Get presigned URL from backend
      const presignRes = await axios.post("/api/videos/presign/", {
        file_name: file.name,
        file_type: file.type,
      });
      const { data, file_url } = presignRes.data;

      // 2. Upload file to S3
      await axios.post(data.url, file, {
        headers: { "Content-Type": file.type },
        data: data.fields,
      });

      // 3. Notify backend to create LectureVideo & start processing
      const lectureRes = await axios.post("/api/videos/start-processing/", {
        s3_key: data.fields.key,
        title: file.name,
      });

      setVideoId(lectureRes.data.video_id);
      setStatus("processing");

    } catch (err) {
      console.error(err);
      alert("Upload failed!");
    } finally {
      setUploading(false);
    }
  };

  // --- Poll for processing status ---
  useEffect(() => {
    let interval;
    if (videoId) {
      interval = setInterval(async () => {
        try {
          const res = await axios.get(`/api/videos/status/${videoId}/`);
          setStatus(res.data.status);

          if (res.data.status === "done") {
            setTranscript(res.data.transcript);
            setSummary(res.data.summary);
            setQuiz(res.data.quiz_questions);
            clearInterval(interval);
          }
        } catch (err) {
          console.error(err);
        }
      }, 5000); // every 5 seconds
    }
    return () => clearInterval(interval);
  }, [videoId]);

  return (
    <div style={{ maxWidth: "800px", margin: "0 auto", padding: "20px" }}>
      <h2>Upload Lecture Video</h2>
      <input type="file" accept="video/*" onChange={handleFileChange} />
      <button onClick={handleUpload} disabled={uploading}>
        {uploading ? "Uploading..." : "Upload & Process"}
      </button>

      {status && <p>Status: {status}</p>}

      {status === "done" && (
        <div>
          <h3>Transcript</h3>
          <pre style={{ whiteSpace: "pre-wrap", background: "#f2f2f2", padding: "10px" }}>
            {transcript}
          </pre>

          <h3>Summary</h3>
          <p>{summary}</p>

          <h3>Quiz Questions</h3>
          <ol>
            {quiz.map((q, idx) => (
              <li key={idx}>
                <strong>{q.question}</strong>
                {q.options && (
                  <ul>
                    {q.options.map((opt, i) => (
                      <li key={i}>{opt}</li>
                    ))}
                  </ul>
                )}
                <p><em>Answer:</em> {q.answer} | <em>Bloom:</em> {q.bloom_level}</p>
              </li>
            ))}
          </ol>
        </div>
      )}
    </div>
  );
};

export default UploadVideo;
