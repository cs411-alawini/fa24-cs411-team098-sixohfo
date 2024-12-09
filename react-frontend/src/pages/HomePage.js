import React, { useState } from 'react';
import axios from 'axios';
import './HomePage.css';  // Import the CSS for styling

const HomePage = () => {
  const [url, setUrl] = useState('');
  const [entities, setEntities] = useState({ books: [], companies: [], people: [] });
  const [error, setError] = useState('');

  const handleUrlChange = (e) => {
    setUrl(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/analyze', { url });
      setEntities(response.data);
      setError('');
    } catch (err) {
      setError('Failed to fetch entities. Please check the URL or try again.');
    }
  };

  return (
    <div className="homepage">
      <h1>Podcast Entity Analyzer</h1>
      <form onSubmit={handleSubmit} className="url-form">
        <input
          type="text"
          placeholder="Enter YouTube podcast URL"
          value={url}
          onChange={handleUrlChange}
          className="url-input"
        />
        <button type="submit" className="submit-button">Analyze</button>
      </form>

      {error && <p className="error-message">{error}</p>}

      <div className="entities-container">
        <div className="entities">
          <h2>Books</h2>
          {entities.books.length > 0 ? (
            entities.books.map((book, index) => (
              <div className="entity-card" key={index}>
                <h3>{book}</h3>
              </div>
            ))
          ) : (
            <p>No books found</p>
          )}
        </div>

        <div className="entities">
          <h2>Companies</h2>
          {entities.companies.length > 0 ? (
            entities.companies.map((company, index) => (
              <div className="entity-card" key={index}>
                <h3>{company}</h3>
              </div>
            ))
          ) : (
            <p>No companies found</p>
          )}
        </div>

        <div className="entities">
          <h2>People</h2>
          {entities.people.length > 0 ? (
            entities.people.map((person, index) => (
              <div className="entity-card" key={index}>
                <h3>{person}</h3>
              </div>
            ))
          ) : (
            <p>No people found</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default HomePage;
