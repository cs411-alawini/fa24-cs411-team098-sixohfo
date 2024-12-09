import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';  // Import the LoginPage component
import HomePage from './pages/HomePage';    // Import the HomePage component

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);  // Track login state

  // Function to handle successful login/signup
  const handleAuthSuccess = () => {
    setIsAuthenticated(true);  // Set authenticated state to true
  };

  return (
    <Router>
      <Routes>
        {/* If user is authenticated, show the HomePage, otherwise redirect to Login */}
        <Route path="/home" element={isAuthenticated ? <HomePage /> : <Navigate to="/" />} />
        
        {/* Login/Signup page */}
        <Route path="/" element={<LoginPage onAuthSuccess={handleAuthSuccess} />} />
        
        {/* Default route to redirect to login/signup page */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
};

export default App;
