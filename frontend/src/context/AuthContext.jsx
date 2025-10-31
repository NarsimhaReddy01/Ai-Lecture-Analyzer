import React, { createContext, useState, useEffect, useContext } from "react";
import { API } from "../services/api";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Load user profile on start
  useEffect(() => {
    const fetchUser = async () => {
      const token = localStorage.getItem("accessToken");
      if (!token) {
        setLoading(false);
        return;
      }

      try {
        const res = await API.get("/auth/profile/");
        setUser(res.data);
      } catch (err) {
        console.error("Auth fetch failed:", err);
        localStorage.removeItem("accessToken");
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, []);

  const login = async (email, password) => {
    const res = await API.post("/auth/login/", { email, password });
    localStorage.setItem("accessToken", res.data.access);
    setUser(res.data.user);
  };

  const logout = () => {
    localStorage.removeItem("accessToken");
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
