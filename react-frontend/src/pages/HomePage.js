import React, { useState } from "react";
import Card from "../components/Card";
import Header from "../components/Header";

const HomePage = ({ isFavorited, setIsFavorited }) => {
  const [search, setSearch] = useState("");

  const cards = [
    { title: "Book, Company, Person", description: "Lorem ipsum dolor sit amet..." },
    { title: "Book, Company, Person", description: "Lorem ipsum dolor sit amet..." },
    { title: "Book, Company, Person", description: "Lorem ipsum dolor sit amet..." },
    { title: "Book, Company, Person", description: "Lorem ipsum dolor sit amet..." },
    { title: "Book, Company, Person", description: "Lorem ipsum dolor sit amet..." },
    { title: "Book, Company, Person", description: "Lorem ipsum dolor sit amet..." },
    { title: "Book, Company, Person", description: "Lorem ipsum dolor sit amet..." },
    { title: "Book, Company, Person", description: "Lorem ipsum dolor sit amet..." },
    { title: "Book, Company, Person", description: "Lorem ipsum dolor sit amet..." },
    { title: "Book, Company, Person", description: "Lorem ipsum dolor sit amet..." },
  ];

  return (
    <div>
      <Header
        page="home"
        onSearchChange={(e) => setSearch(e.target.value)}
        isFavorited={isFavorited}
        onFavoriteToggle={() => setIsFavorited(!isFavorited)}
      />
      <div className="card-container">
        {cards
          .filter((card) => card.title.toLowerCase().includes(search.toLowerCase()))
          .map((card) => (
            <Card
              key={card.title}
              title={card.title}
              description={card.description}
            />
          ))}
      </div>
    </div>
  );
};

export default HomePage;
