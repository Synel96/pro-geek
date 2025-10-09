import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { CssVarsProvider } from "@mui/joy/styles";
import theme from "./themes/theme";
import Navbar from "./components/pictures/navbar/Navbar";
import LoginPage from "./pages/LoginPage";
import Footer from "./components/footer/Footer";

function AppContent() {
  return (
    <CssVarsProvider defaultMode="dark" theme={theme}>
      <BrowserRouter>
        <div
          style={{
            minHeight: "100vh",
            display: "flex",
            flexDirection: "column",
          }}
        >
          <Navbar />
          <div style={{ flex: 1 }}>
            <Routes>
              <Route path="/bejelentkezes" element={<LoginPage />} />
            </Routes>
          </div>
          <Footer />
        </div>
      </BrowserRouter>
    </CssVarsProvider>
  );
}

export default function App() {
  return <AppContent />;
}
