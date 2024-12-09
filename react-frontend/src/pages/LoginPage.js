import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './LoginPage.css'; // Import the CSS file for styling

const LoginPage = ({ onAuthSuccess }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [isSignUp, setIsSignUp] = useState(false); // State to toggle between login and signup

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('http://localhost:8000/valid_user', {
        username: username,
        password: password,
      });

      if (response.data.message && response.data.message.includes('Welcome back')) {
        setSuccessMessage(response.data.message);
        setErrorMessage('');
        onAuthSuccess();
        navigate('/home');
      } else {
        setErrorMessage(response.data.message || 'An error occurred. Please try again.');
        setSuccessMessage('');
      }
    } catch (err) {
      setErrorMessage('An error occurred. Please try again.');
      setSuccessMessage('');
    }
  };

  const handleSignUpSubmit = async (e) => {
    e.preventDefault();
    

    const user_id = Math.floor(Math.random() * (1000 - 20 + 1)) + 20;

    try {
      const response = await axios.post('http://localhost:8000/add_user', {
        user_id: user_id,
        username: username,
        password: password,
      });

      if (response.data.message) {
        setSuccessMessage(response.data.message);
        setErrorMessage('');
        setIsSignUp(false);  // Toggle back to login after successful sign-up
      }
    } catch (err) {
      setErrorMessage('An error occurred during sign-up. Please try again.');
      setSuccessMessage('');
    }
  };

  return (
    <div className="login-container">
      <h1>{isSignUp ? 'Sign Up' : 'Login'}</h1>
      <form onSubmit={isSignUp ? handleSignUpSubmit : handleSubmit} className="form-container">
        <div className="form-group">
          <label htmlFor="username">Username:</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="form-input"
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="form-input"
            required
          />
        </div>
        <button type="submit" className="submit-btn">{isSignUp ? 'Sign Up' : 'Login'}</button>
      </form>
      {errorMessage && <div className="error-message">{errorMessage}</div>}
      {successMessage && <div className="success-message">{successMessage}</div>}

      <button onClick={() => setIsSignUp(!isSignUp)} className="toggle-btn">
        {isSignUp ? 'Already have an account? Login' : 'Don’t have an account? Sign Up'}
      </button>
    </div>
  );
};

export default LoginPage;
