import React from "react";
import Card from "../components/Card";
import Header from "../components/Header";

const FavoritesPage = ({ isFavorited }) => {
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
      <Header page="favorites" />
      <div className="card-container">
        {isFavorited ? (
          cards.map((card) => (
            <Card
              key={card.title}
              title={card.title}
              description={card.description}
            />
          ))
        ) : (
          <p style={{ textAlign: "center", marginTop: "20px" }}>
            No favorite podcasts yet.
          </p>
        )}
      </div>
    </div>
  );
};

export default FavoritesPage;