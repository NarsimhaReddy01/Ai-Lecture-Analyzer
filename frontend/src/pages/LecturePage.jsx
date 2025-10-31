import React, { useState, useEffect } from "react";
import { API } from "../services/api";
import { useParams } from "react-router-dom";

const LecturePage = () => {
  const { id } = useParams(); // video ID passed via route
  const [videoData, setVideoData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchVideoData = async () => {
      try {
        const res = await API.get(`/videos/${id}/`);
        setVideoData(res.data);
      } catch (err) {
        console.error(err);
        setError("Failed to load video data. Please try again later.");
      } finally {
        setLoading(false);
      }
    };
    fetchVideoData();
  }, [id]);

  if (loading)
    return (
      <div className="flex justify-center items-center h-screen text-blue-700 font-semibold text-xl">
        Loading lecture details...
      </div>
    );

  if (error)
    return (
      <div className="text-center text-red-600 font-semibold mt-20">
        ❌ {error}
      </div>
    );

  if (!videoData)
    return (
      <div className="text-center text-gray-600 mt-20">
        No video data found.
      </div>
    );

  return (
    <div className="min-h-screen bg-gray-50 text-gray-800">
      {/* --- HEADER --- */}
      <div className="bg-blue-700 text-white py-4 shadow-md">
        <h1 className="text-2xl font-bold text-center">
          🎓 {videoData.title || "Lecture Analysis"}
        </h1>
      </div>

      <div className="max-w-7xl mx-auto p-6 grid md:grid-cols-3 gap-6">
        {/* --- VIDEO PLAYER --- */}
        <div className="md:col-span-2 bg-white shadow-md rounded-lg p-4">
          <h2 className="text-lg font-semibold text-blue-700 mb-3">
            🎥 Lecture Playback
          </h2>
          <video
            controls
            src={videoData.video_url}
            className="w-full rounded-lg shadow"
          />
        </div>

        {/* --- SUMMARY --- */}
        <div className="bg-white shadow-md rounded-lg p-4 overflow-y-auto">
          <h2 className="text-lg font-semibold text-blue-700 mb-3">
            🧠 Lecture Summary
          </h2>
          <p className="text-sm leading-relaxed whitespace-pre-line">
            {videoData.summary || "Summary not available yet."}
          </p>
        </div>

        {/* --- TRANSCRIPTS (ENGLISH & HINDI) --- */}
        <div className="md:col-span-2 bg-white shadow-md rounded-lg p-4 mt-4">
          <h2 className="text-lg font-semibold text-blue-700 mb-3">
            🗣️ Bilingual Transcript
          </h2>

          <div className="flex flex-col md:flex-row gap-4">
            {/* English */}
            <div className="flex-1 border rounded-md p-3 overflow-y-auto max-h-80">
              <h3 className="text-blue-600 font-medium mb-2">English</h3>
              <pre className="text-sm whitespace-pre-wrap">
                {videoData.transcript_en || "English transcript not yet available."}
              </pre>
            </div>

            {/* Hindi */}
            <div className="flex-1 border rounded-md p-3 overflow-y-auto max-h-80">
              <h3 className="text-blue-600 font-medium mb-2">Hindi</h3>
              <pre className="text-sm whitespace-pre-wrap">
                {videoData.transcript_hi || "Hindi transcript not yet available."}
              </pre>
            </div>
          </div>
        </div>

        {/* --- QUIZ SECTION --- */}
        <div className="bg-white shadow-md rounded-lg p-4 mt-4">
          <h2 className="text-lg font-semibold text-blue-700 mb-3">
            🧩 Quiz Section
          </h2>

          {videoData.quiz && videoData.quiz.length > 0 ? (
            <div className="space-y-4">
              {videoData.quiz.map((q, idx) => (
                <div key={idx} className="border p-3 rounded-md">
                  <p className="font-medium mb-2">
                    Q{idx + 1}. {q.question}
                  </p>
                  {q.options && (
                    <ul className="space-y-1">
                      {q.options.map((opt, i) => (
                        <li
                          key={i}
                          className="px-2 py-1 border rounded cursor-pointer hover:bg-blue-50"
                        >
                          {opt}
                        </li>
                      ))}
                    </ul>
                  )}
                  {q.answer && (
                    <p className="text-green-600 text-sm mt-2">
                      ✅ Correct Answer: {q.answer}
                    </p>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-gray-500">
              Quiz will be generated automatically after processing.
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default LecturePage;
