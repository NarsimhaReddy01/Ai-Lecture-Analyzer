import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import App from "./App.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import UploadPage from "./pages/UploadPage.jsx";
import AdminPanel from "./pages/AdminPanel.jsx";
import { AuthProvider } from "./context/AuthContext.jsx";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<App />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/upload" element={<UploadPage />} />
          <Route path="/admin" element={<AdminPanel />} />
        </Routes>
      </Router>
    </AuthProvider>
  </React.StrictMode>
);
