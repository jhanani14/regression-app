import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Auth from "./pages/Auth";
import Upload from "./pages/Upload";
import Configure from "./pages/Configure";
import Results from "./pages/Results";
import History from "./pages/History";
import DashboardLayout from "./layouts/DashboardLayout";

function PrivateRoute({ children }: { children: React.ReactNode }) {
  const token = localStorage.getItem("token");
  return token ? children : <Navigate to="/auth" replace />;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Route */}
        <Route path="/auth" element={<Auth />} />

        {/* Private Routes */}
        <Route
          path="/upload"
          element={
            <PrivateRoute>
              <DashboardLayout>
                <Upload />
              </DashboardLayout>
            </PrivateRoute>
          }
        />
        <Route
          path="/configure"
          element={
            <PrivateRoute>
              <DashboardLayout>
                <Configure />
              </DashboardLayout>
            </PrivateRoute>
          }
        />
        <Route
          path="/results/:id"
          element={
            <PrivateRoute>
              <DashboardLayout>
                <Results />
              </DashboardLayout>
            </PrivateRoute>
          }
        />
        <Route
          path="/history"
          element={
            <PrivateRoute>
              <DashboardLayout>
                <History />
              </DashboardLayout>
            </PrivateRoute>
          }
        />

        {/* Default Redirects */}
        <Route path="/" element={<Navigate to="/upload" replace />} />
        <Route path="*" element={<Navigate to="/auth" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
