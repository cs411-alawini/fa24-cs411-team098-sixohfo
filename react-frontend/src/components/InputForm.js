// src/components/InputForm.js
import React, { useState } from 'react';

const InputForm = ({ fetchEntities, loading }) => {
  const [url, setUrl] = useState('');

  const handleInputChange = (e) => {
    setUrl(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    fetchEntities(url);
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter YouTube podcast URL"
          value={url}
          onChange={handleInputChange}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? "Loading..." : "Analyze Podcast"}
        </button>
      </form>
    </div>
  );
};

export default InputForm;
