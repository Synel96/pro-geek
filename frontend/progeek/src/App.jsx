import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

function Home() {
  return <h1>Főoldal</h1>;
}

function About() {
  return <h1>Rólunk</h1>;
}

export default function App() {
  return (
    <BrowserRouter>
      <div></div>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </BrowserRouter>
  );
}
