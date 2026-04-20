import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useEffect } from "react";
import { wakeBackend } from "./services/api";
import AuthProvider from "./context/AuthContext";

import Login from "./components/Login";
import SkillDetail from "./components/SkillDetail";

import Dashboard from "./pages/Dashboard";
import Analytics from "./pages/Analytics";
import Reminders from "./pages/Reminders";
import Profile from "./pages/Profile";
import SkillHistory from "./pages/SkillHistory";

import ProtectedRoute from "./components/ProtectedRoute";

export default function App() {
  // 🔥 Proactively wake the backend on first load
  useEffect(() => {
    wakeBackend();
  }, []);

  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          {/* Public Routes */}
          <Route path="/" element={<Login />} />

          {/* Protected Routes */}
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />

          <Route
            path="/analytics"
            element={
              <ProtectedRoute>
                <Analytics />
              </ProtectedRoute>
            }
          />

          <Route
            path="/reminders"
            element={
              <ProtectedRoute>
                <Reminders />
              </ProtectedRoute>
            }
          />

          <Route
            path="/profile"
            element={
              <ProtectedRoute>
                <Profile />
              </ProtectedRoute>
            }
          />

          {/* Skill Routes */}
          <Route
            path="/skill/:id"
            element={
              <ProtectedRoute>
                <SkillDetail />
              </ProtectedRoute>
            }
          />

          <Route
            path="/skill/:id/history"
            element={
              <ProtectedRoute>
                <SkillHistory />
              </ProtectedRoute>
            }
          />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}