import React from 'react';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from './pages/Home';
import About from './pages/About';
import Layout from './components/Layout';
import View from './View';
import { AuthProvider } from './components/AuthContext';
import PrivateChatRoute from './components/PrivateChatRoute';


function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route element={<PrivateChatRoute />}>
                    <Route path="/chat" element={<Layout><View /></Layout>} />
                </Route>
          <Route path="/about" element={<Layout><About /></Layout>} />
        </Routes>
        </BrowserRouter>
      </AuthProvider>
  );
}

export default App;



