import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const Navbar = () => {
  const { user, logout } = useAuth();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/auth/login");
  };

  return (
    <nav className="bg-white dark:bg-gray-900 shadow-md fixed top-0 left-0 w-full z-50">
      <div className="container mx-auto px-6 py-3 flex justify-between items-center">
        {/* Logo */}
        <Link to="/" className="text-2xl font-bold text-blue-600">
          🎓 JEEVIC AI
        </Link>

        {/* Mobile menu button */}
        <button
          onClick={() => setIsMenuOpen(!isMenuOpen)}
          className="md:hidden text-gray-800 dark:text-gray-200 focus:outline-none"
        >
          {isMenuOpen ? "✖" : "☰"}
        </button>

        {/* Menu Links */}
        <div
          className={`${
            isMenuOpen ? "block" : "hidden"
          } absolute md:static top-14 left-0 md:flex md:space-x-6 bg-white dark:bg-gray-900 md:bg-transparent w-full md:w-auto shadow-md md:shadow-none p-4 md:p-0`}
        >
          {user ? (
            <>
              <Link
                to="/dashboard"
                className="block py-2 md:py-0 hover:text-blue-600 dark:hover:text-blue-400"
                onClick={() => setIsMenuOpen(false)}
              >
                Dashboard
              </Link>

              <Link
                to="/lecture"
                className="block py-2 md:py-0 hover:text-blue-600 dark:hover:text-blue-400"
                onClick={() => setIsMenuOpen(false)}
              >
                Lectures
              </Link>

              <Link
                to="/upload"
                className="block py-2 md:py-0 hover:text-blue-600 dark:hover:text-blue-400"
                onClick={() => setIsMenuOpen(false)}
              >
                Upload
              </Link>

              {user.is_admin && (
                <Link
                  to="/admin"
                  className="block py-2 md:py-0 hover:text-blue-600 dark:hover:text-blue-400"
                  onClick={() => setIsMenuOpen(false)}
                >
                  Admin
                </Link>
              )}

              <button
                onClick={handleLogout}
                className="block w-full text-left md:w-auto bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md mt-2 md:mt-0"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link
                to="/auth/login"
                className="block py-2 md:py-0 hover:text-blue-600 dark:hover:text-blue-400"
                onClick={() => setIsMenuOpen(false)}
              >
                Login
              </Link>

              <Link
                to="/auth/signup"
                className="block py-2 md:py-0 hover:text-blue-600 dark:hover:text-blue-400"
                onClick={() => setIsMenuOpen(false)}
              >
                Signup
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
