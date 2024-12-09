import React, { useState } from 'react';
import axios from 'axios';
import './HomePage.css';

const HomePage = () => {
  const [url, setUrl] = useState('');
  const [entities, setEntities] = useState({ books: [], companies: [], people: [] });
  const [error, setError] = useState('');
  const [extraInfo, setExtraInfo] = useState({});
  const [mostMentionedCompanies, setMostMentionedCompanies] = useState([]);
  const [mostMentionedBooks, setMostMentionedBooks] = useState([]);

  const handleUrlChange = (e) => {
    setUrl(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/analyze', { url });
      setEntities(response.data);
      setError('');
      setExtraInfo({});
    } catch (err) {
      setError('Failed to fetch entities. Please check the URL or try again.');
    }
  };

  const handleCardClick = async (type, entity) => {
    try {
      const response = await axios.post('http://localhost:8000/check_db_for_string', {
        type,
        entity,
      });
  
      // Extract the message and result from the response
      const { message, result } = response.data;
      
      // Format the result array into a string
      const formattedResult = result.join(' - '); // You can change the separator if needed
  
      // Update the state with the formatted string
      setExtraInfo((prev) => ({
        ...prev,
        [`${type}-${entity}`]: `${message}: ${formattedResult}`,
      }));
    } catch (err) {
      console.error('Failed to fetch additional info:', err);
    }
  };
  

  const fetchMostMentionedCompanies = async () => {
    try {
      const response = await axios.get('http://localhost:8000/most_mentioned_companies_with_revenue');
      setMostMentionedCompanies(response.data);
    } catch (err) {
      console.error('Failed to fetch most mentioned companies:', err);
    }
  };

  const fetchMostMentionedBooks = async () => {
    try {
      const response = await axios.get('http://localhost:8000/most_mentioned_books');
      setMostMentionedBooks(response.data);
    } catch (err) {
      console.error('Failed to fetch most mentioned books:', err);
    }
  };

  return (
    <div className="homepage">
      <div className="header-buttons">
        <button onClick={fetchMostMentionedCompanies} className="header-button">
          Most Mentioned Companies
        </button>
        <button onClick={fetchMostMentionedBooks} className="header-button">
          Most Mentioned Books
        </button>
      </div>

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
        {['books', 'companies', 'people'].map((type) => (
          <div className="entities" key={type}>
            <h2>{type.charAt(0).toUpperCase() + type.slice(1)}</h2>
            {entities[type].length > 0 ? (
              entities[type].map((entity, index) => (
                <div
                  className="entity-card"
                  key={index}
                  onClick={() => handleCardClick(type, entity)}
                >
                  <h3>{entity}</h3>
                  {extraInfo[`${type}-${entity}`] && (
                    <p className="extra-info">{extraInfo[`${type}-${entity}`]}</p>
                  )}
                </div>
              ))
            ) : (
              <p>No {type} found</p>
            )}
          </div>
        ))}
      </div>


      {mostMentionedCompanies.length > 0 && (
        <div className="most-mentioned">
          <h2>Most Mentioned Companies with Total Revenue in Millions</h2>
          <ul>
            {mostMentionedCompanies.map((company, index) => (
              <li key={index}>
                {company.CompanyName} - Mentions: {company.MentionCount}, Revenue: {company.TotalRevenue}
              </li>
            ))}
          </ul>
        </div>
      )}

      {mostMentionedBooks.length > 0 && (
        <div className="most-mentioned">
          <h2>Most Mentioned Books</h2>
          <ul>
            {mostMentionedBooks.map((book, index) => (
              <li key={index}>
                {book.BookName} - Mentions: {book.MentionCount}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default HomePage;
