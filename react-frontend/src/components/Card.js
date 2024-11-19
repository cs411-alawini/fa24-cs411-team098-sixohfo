import React from "react";
import "./Card.css";

const Card = ({ title, description }) => {
  return (
    <div className="card">
      <h2>{title}</h2>
      <div className="image-placeholder">IMG</div>
      <p>{description}</p>
    </div>
  );
};

export default Card;
