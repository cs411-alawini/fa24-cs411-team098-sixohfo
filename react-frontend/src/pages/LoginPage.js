import React, { useState } from 'react';
import axios from 'axios';
import './LoginPage.css';  // Import CSS for styling

const LoginPage = ({ onAuthSuccess }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  // Handle form submission for login/signup (since both are handled the same way)
  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('http://localhost:5000/auth', {
        username,
        password,
      });

      if (response.data.success) {
        setSuccessMessage(response.data.message); // Show success message (login or signup)
        setErrorMessage('');
        onAuthSuccess();  // Call onAuthSuccess to navigate to HomePage
      } else {
        setErrorMessage(response.data.message || 'An error occurred. Please try again.');
        setSuccessMessage('');
      }
    } catch (err) {
      setErrorMessage('An error occurred. Please try again.');
      setSuccessMessage('');
    }
  };

  return (
    <div className="login-page">
      <h1>Welcome to the App</h1>
      <form className="login-form">
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="input-field"
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="input-field"
          required
        />

        {/* Button to either login or sign up (both handled in the same way) */}
        <button 
          type="submit" 
          className="submit-button"
          onClick={handleSubmit}  
        >
          Login / Sign Up
        </button>
      </form>

      {errorMessage && <p className="error-message">{errorMessage}</p>}
      {successMessage && <p className="success-message">{successMessage}</p>}
    </div>
  );
};

export default LoginPage;
