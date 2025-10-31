import React from "react";

/**
 * ProgressCard — Reusable stats card used in the student dashboard
 * Props:
 *  - title: string
 *  - value: string or number
 *  - color: optional Tailwind color (default blue)
 *  - icon: optional React component (Lucide / Heroicon)
 */
const ProgressCard = ({ title, value, color = "blue", icon: Icon }) => {
  return (
    <div
      className={`flex items-center justify-between bg-white shadow-md rounded-xl p-5 border-l-4 border-${color}-500 hover:shadow-lg transition-shadow`}
    >
      <div>
        <h3 className="text-sm text-gray-500 font-semibold uppercase">
          {title}
        </h3>
        <p className="text-2xl font-bold text-gray-800 mt-1">{value}</p>
      </div>
      {Icon && (
        <div className={`text-${color}-500 text-3xl`}>
          <Icon />
        </div>
      )}
    </div>
  );
};

export default ProgressCard;
