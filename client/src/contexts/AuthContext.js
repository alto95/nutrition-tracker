import React, { createContext, useState, useEffect } from 'react';
import { loginUser, registerUser, getCurrentUser, loginWithGoogle } from '../services/authService';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const checkUserLoggedIn = async () => {
      try {
        const token = localStorage.getItem('token');
        if (token) {
          const userData = await getCurrentUser();
          setCurrentUser(userData);
        }
      } catch (err) {
        console.error('Error checking authentication:', err);
        localStorage.removeItem('token');
      } finally {
        setLoading(false);
      }
    };

    checkUserLoggedIn();
  }, []);

  const login = async (email, password) => {
    try {
      setError(null);
      const data = await loginUser(email, password);
      localStorage.setItem('token', data.token);
      setCurrentUser(data.user);
      return data.user;
    } catch (err) {
      setError(err.message || 'Failed to login');
      throw err;
    }
  };

  const googleLogin = async (tokenId) => {
    try {
      setError(null);
      const data = await loginWithGoogle(tokenId);
      localStorage.setItem('token', data.token);
      setCurrentUser(data.user);
      return data.user;
    } catch (err) {
      setError(err.message || 'Failed to login with Google');
      throw err;
    }
  };

  const register = async (name, email, password) => {
    try {
      setError(null);
      const data = await registerUser(name, email, password);
      localStorage.setItem('token', data.token);
      setCurrentUser(data.user);
      return data.user;
    } catch (err) {
      setError(err.message || 'Failed to register');
      throw err;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setCurrentUser(null);
  };

  const value = {
    currentUser,
    loading,
    error,
    login,
    googleLogin,
    register,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
