import React from "react";

const TranscriptView = ({ transcript }) => {
  return (
    <div className="bg-white dark:bg-gray-900 p-4 rounded-xl shadow-sm h-[60vh] overflow-y-auto">
      <h2 className="text-lg font-semibold mb-3">🗣 Transcript</h2>
      {transcript?.length ? (
        transcript.map((line, i) => (
          <p
            key={i}
            className="text-gray-700 dark:text-gray-200 mb-2 hover:bg-gray-100 dark:hover:bg-gray-800 p-1 rounded transition"
          >
            <span className="text-xs text-gray-500">[{line.timestamp}]</span>{" "}
            {line.text}
          </p>
        ))
      ) : (
        <p className="text-gray-500 italic">No transcript available.</p>
      )}
    </div>
  );
};

export default TranscriptView;
