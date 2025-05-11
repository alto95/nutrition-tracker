import React, { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../contexts/AuthContext';

const Navbar = () => {
  const { currentUser, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <Link to="/" className="navbar-brand">Nutrition Tracker</Link>
      
      <ul className="navbar-menu">
        {currentUser ? (
          <>
            <li><Link to="/dashboard">Dashboard</Link></li>
            <li><Link to="/meals">Meals</Link></li>
            <li><Link to="/glucose">Glucose</Link></li>
            <li className="user-menu">
              <Link to="/profile">Profile</Link>
            </li>
            <li><button onClick={handleLogout} className="btn btn-link">Logout</button></li>
          </>
        ) : (
          <>
            <li><Link to="/login">Login</Link></li>
            <li><Link to="/register">Register</Link></li>
          </>
        )}
      </ul>
    </nav>
  );
};

export default Navbar;
