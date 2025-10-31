import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";

import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import UploadForm from "./components/UploadForm";
import VideoList from "./components/VideoList";
import VideoDetails from "./components/VideoDetails";

import UploadPage from "./pages/UploadPage";
import LecturePage from "./pages/LecturePage";
import Dashboard from "./pages/Dashboard";
import AdminPanel from "./pages/AdminPanel";
import Login from "./pages/Login";
import Signup from "./pages/Signup";

import ProtectedRoute from "./components/ProtectedRoute";
import { AuthProvider } from "./context/AuthContext";

function App() {
  const [selectedVideo, setSelectedVideo] = useState(null);
  const [refresh, setRefresh] = useState(false);

  return (
    <AuthProvider>
      <Router>
        <Navbar />

        <Routes>
          {/* 🔐 Auth Routes */}
          <Route path="/" element={<Navigate to="/auth/login" replace />} />
          <Route path="/auth/login" element={<Login />} />
          <Route path="/auth/signup" element={<Signup />} />

          {/* ✅ Unified Lecture Page (existing components combined here) */}
          <Route
            path="/lecture"
            element={
              <ProtectedRoute>
                <div className="min-h-screen bg-gray-50 dark:bg-gray-950 p-8">
                  <h1 className="text-3xl font-bold text-center mb-8 text-blue-700">
                    🎓 AI Lecture Analyzer
                  </h1>
                  <div className="grid md:grid-cols-3 gap-6">
                    <div>
                      <UploadForm onUploadComplete={() => setRefresh(!refresh)} />
                      <VideoList key={refresh} onSelectVideo={setSelectedVideo} />
                    </div>
                    <div className="md:col-span-2">
                      <VideoDetails videoId={selectedVideo} />
                    </div>
                  </div>
                </div>
              </ProtectedRoute>
            }
          />

          {/* 📤 Upload Page */}
          <Route
            path="/upload"
            element={
              <ProtectedRoute>
                <UploadPage />
              </ProtectedRoute>
            }
          />

          {/* 🎬 Lecture Details (future: /lecture/:id) */}
          <Route
            path="/lecture/:videoId"
            element={
              <ProtectedRoute>
                <LecturePage />
              </ProtectedRoute>
            }
          />

          {/* 📊 Student Dashboard */}
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />

          {/* 🧑‍🏫 Admin Panel */}
          <Route
            path="/admin"
            element={
              <ProtectedRoute>
                <AdminPanel />
              </ProtectedRoute>
            }
          />
        </Routes>

        <Footer />
      </Router>
    </AuthProvider>
  );
}

export default App;
