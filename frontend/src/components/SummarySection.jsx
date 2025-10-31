import React from "react";

const SummarySection = ({ summary }) => {
  return (
    <div className="bg-white dark:bg-gray-900 p-4 rounded-xl shadow-sm">
      <h2 className="text-lg font-semibold mb-3">📘 Summary</h2>
      {summary ? (
        <p className="text-gray-700 dark:text-gray-200 leading-relaxed whitespace-pre-line">
          {summary}
        </p>
      ) : (
        <p className="text-gray-500 italic">Summary not yet generated.</p>
      )}
    </div>
  );
};

export default SummarySection;
