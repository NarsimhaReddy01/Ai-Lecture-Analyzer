import React from "react";
import { Link } from "react-router-dom";

const Footer = () => {
  return (
    <footer className="bg-gray-100 dark:bg-gray-950 text-gray-700 dark:text-gray-300 mt-16 border-t border-gray-300 dark:border-gray-800">
      <div className="container mx-auto px-6 py-6 flex flex-col md:flex-row justify-between items-center">
        <div className="text-center md:text-left mb-3 md:mb-0">
          <p className="text-sm">
            © {new Date().getFullYear()} <span className="font-semibold">JEEVIC AI Lecture Analyzer</span>.  
            All Rights Reserved.
          </p>
        </div>

        <div className="flex space-x-4 text-sm">
          <Link
            to="/dashboard"
            className="hover:text-blue-600 dark:hover:text-blue-400"
          >
            Dashboard
          </Link>
          <Link
            to="/lecture"
            className="hover:text-blue-600 dark:hover:text-blue-400"
          >
            Lectures
          </Link>
          <Link
            to="/upload"
            className="hover:text-blue-600 dark:hover:text-blue-400"
          >
            Upload
          </Link>
          <a
            href="mailto:support@jeevic.ai"
            className="hover:text-blue-600 dark:hover:text-blue-400"
          >
            Contact
          </a>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
