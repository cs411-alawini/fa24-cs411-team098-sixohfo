import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import FavoritesPage from "./pages/FavoritesPage";

const App = () => {
  const [isFavorited, setIsFavorited] = useState(false); // State for the podcast favorite status

  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={<HomePage isFavorited={isFavorited} setIsFavorited={setIsFavorited} />}
        />
        <Route
          path="/favorites"
          element={<FavoritesPage isFavorited={isFavorited} />}
        />
      </Routes>
    </Router>
  );
};

export default App;
