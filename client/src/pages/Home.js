import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className="home-page">
      <div className="hero">
        <h1>Track Your Nutrition and Glucose Levels</h1>
        <p>Take control of your health with our comprehensive tracking tool</p>
        <Link to="/register" className="btn btn-primary">Get Started</Link>
      </div>
      
      <div className="features">
        <div className="feature-card">
          <h2>Track Meals</h2>
          <p>Log your meals and track calories, carbs, proteins, and fats</p>
        </div>
        
        <div className="feature-card">
          <h2>Monitor Glucose</h2>
          <p>Keep track of your glucose levels throughout the day</p>
        </div>
        
        <div className="feature-card">
          <h2>Analyze Trends</h2>
          <p>Visualize your data with charts and identify patterns</p>
        </div>
      </div>
    </div>
  );
};

export default Home;
