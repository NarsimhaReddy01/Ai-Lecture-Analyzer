import React, { useEffect, useState } from "react";
import axios from "axios";

const VideoDetails = ({ videoId }) => {
  const [videoData, setVideoData] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!videoId) return;

    const fetchDetails = async () => {
      setLoading(true);
      try {
        const res = await axios.get(
          `http://localhost:8000/api/videos/${videoId}/`
        );
        setVideoData(res.data);
      } catch (err) {
        console.error("Error fetching video details:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchDetails();
  }, [videoId]);

  if (!videoId)
    return (
      <div className="text-gray-600 text-center mt-10">
        👈 Select a video to view its details.
      </div>
    );

  if (loading) return <div>Loading video details...</div>;
  if (!videoData) return null;

  const { video_url, transcript_en, transcript_hi, summary, quiz } = videoData;

  return (
    <div className="bg-white shadow-md rounded-lg p-6">
      <h2 className="text-xl font-bold text-blue-700 mb-4">
        🎬 Lecture Details
      </h2>

      {/* Video Player */}
      {video_url ? (
        <video
          controls
          src={video_url}
          className="w-full rounded-lg border mb-6"
        />
      ) : (
        <p className="text-gray-500">No video available.</p>
      )}

      {/* Transcript Section */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold mb-2 text-gray-800">
          🗒 Transcript
        </h3>
        <div className="grid md:grid-cols-2 gap-4 text-sm text-gray-700">
          <div>
            <h4 className="font-medium text-blue-600 mb-1">English</h4>
            <pre className="bg-gray-50 p-3 rounded-md border overflow-x-auto">
              {transcript_en || "No English transcript available."}
            </pre>
          </div>
          <div>
            <h4 className="font-medium text-green-600 mb-1">Hindi</h4>
            <pre className="bg-gray-50 p-3 rounded-md border overflow-x-auto">
              {transcript_hi || "No Hindi transcript available."}
            </pre>
          </div>
        </div>
      </div>

      {/* Summary Section */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold mb-2 text-gray-800">
          🧠 AI-Generated Summary
        </h3>
        <p className="bg-gray-50 p-3 rounded-md border text-gray-700">
          {summary || "Summary not available yet."}
        </p>
      </div>

      {/* Quiz Section */}
      <div>
        <h3 className="text-lg font-semibold mb-2 text-gray-800">🧩 Quiz</h3>
        {quiz && quiz.length > 0 ? (
          <ul className="space-y-3">
            {quiz.map((q, i) => (
              <li
                key={i}
                className="border rounded-md p-3 bg-gray-50 hover:bg-gray-100"
              >
                <p className="font-medium">
                  {i + 1}. {q.question}
                </p>
                {q.options && q.options.length > 0 && (
                  <ul className="ml-5 list-disc text-gray-600 text-sm">
                    {q.options.map((opt, j) => (
                      <li key={j}>{opt}</li>
                    ))}
                  </ul>
                )}
                {q.answer && (
                  <p className="text-sm text-green-700 mt-2">
                    <strong>Answer:</strong> {q.answer}
                  </p>
                )}
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-gray-500">No quiz available for this lecture.</p>
        )}
      </div>
    </div>
  );
};

export default VideoDetails;
