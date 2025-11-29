import React from "react";
import "../../components/component.css";

const App = () => {
  return (
    <div className="app-container">

      {/* HERO / HEADER */}
      <header className="hero">
        <div className="hero-content">
          <h1 className="hero-title">Stay Relevant</h1>
          <p className="hero-subtitle">
            Predict your futures. Enter a year and obtain a prediction of the economic state and growth between those years.
          </p>

          {/* Input + Button Card */}
          <div className="input-card">
            <input
              type="text"
              placeholder="Enter a year..."
              className="user-input"
              form=""
            />
            <button className="generate-btn">Generate</button>
          </div>
        </div>
      </header>

      {/* Developer / Mission Section — more professional */}
      <footer className="footer-section">
        <div className="footer-container">
          <h2>Our Mission</h2>
          <p>
            Our mission is to equip individuals with in-depth insights into economic trends and growth patterns across the United States, fostering informed decision-making, strategic planning, and a clearer understanding of the nation’s financial trajectory.
          </p>

          <h2>Additional Information</h2>
          <p>
            This platform is designed for researchers, students, and professionals who seek reliable data and predictions to guide financial and economic decisions.
          </p>
        </div>
      </footer>

    </div>
  );
};

export default App;