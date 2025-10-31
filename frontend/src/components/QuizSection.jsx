import React, { useState } from "react";

const QuizSection = ({ quiz }) => {
  const [answers, setAnswers] = useState({});

  const handleAnswer = (qid, value) => {
    setAnswers({ ...answers, [qid]: value });
  };

  return (
    <div className="bg-white dark:bg-gray-900 p-6 rounded-xl shadow-lg mt-8">
      <h2 className="text-lg font-semibold mb-4">🧩 Interactive Quiz</h2>
      {quiz?.length ? (
        quiz.map((q, i) => (
          <div key={i} className="mb-6">
            <p className="font-medium mb-2">
              Q{i + 1}. {q.question}
            </p>
            {q.options.map((opt, j) => (
              <label
                key={j}
                className="block cursor-pointer p-2 rounded hover:bg-gray-100 dark:hover:bg-gray-800"
              >
                <input
                  type="radio"
                  name={`q-${i}`}
                  value={opt}
                  checked={answers[i] === opt}
                  onChange={() => handleAnswer(i, opt)}
                  className="mr-2"
                />
                {opt}
              </label>
            ))}
          </div>
        ))
      ) : (
        <p className="text-gray-500 italic">No quiz generated yet.</p>
      )}
      <button className="bg-blue-600 text-white px-5 py-2 rounded-lg hover:bg-blue-700 transition">
        Submit Answers
      </button>
    </div>
  );
};

export default QuizSection;
