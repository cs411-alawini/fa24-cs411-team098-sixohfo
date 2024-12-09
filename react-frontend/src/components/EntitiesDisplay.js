// src/components/EntitiesDisplay.js
import React from 'react';
import Card from './Card';

const EntitiesDisplay = ({ entities }) => {
  return (
    <div>
      <h2>Books</h2>
      <div className="cards-container">
        {entities.books.map((book, index) => (
          <Card key={index} type="Book" entity={book} />
        ))}
      </div>

      <h2>Companies</h2>
      <div className="cards-container">
        {entities.companies.map((company, index) => (
          <Card key={index} type="Company" entity={company} />
        ))}
      </div>

      <h2>People</h2>
      <div className="cards-container">
        {entities.people.map((person, index) => (
          <Card key={index} type="Person" entity={person} />
        ))}
      </div>
    </div>
  );
};

export default EntitiesDisplay;
