// src/components/Card.js
const Card = ({ type, entity }) => {
  return (
    <div className="card">
      <h3>{type}: {entity}</h3>
    </div>
  );
};

export default Card;
