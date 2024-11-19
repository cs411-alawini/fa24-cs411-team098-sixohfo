import React from "react";
import { useNavigate } from "react-router-dom";
import { FaStar, FaRegStar } from "react-icons/fa"; // Import star icons
import "./Header.css";

const Header = ({ page, onSearchChange, isFavorited, onFavoriteToggle }) => {
  const navigate = useNavigate();

  return (
    <header className="header">
      {page === "home" && (
        <>
          <div></div> {/* Empty placeholder for alignment */}
          <div className="header-middle">
            <input
              type="text"
              className="search-input"
              placeholder="Search here..."
              onChange={onSearchChange}
            />
            <button className="favorite-star" onClick={onFavoriteToggle}>
              {isFavorited ? <FaStar color="#ffc107" /> : <FaRegStar color="#ccc" />}
            </button>
          </div>
          <button className="nav-button" onClick={() => navigate("/favorites")}>
            Favorites
          </button>
        </>
      )}
      {page === "favorites" && (
        <>
          <button className="nav-button" onClick={() => console.log("Visualize")}>
            Visualization
          </button>
          <h1 className="header-title">Favorites</h1>
          <button className="nav-button" onClick={() => navigate("/")}>
            Home
          </button>
        </>
      )}
    </header>
  );
};

export default Header;
