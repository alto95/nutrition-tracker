import React, { createContext, useState, useEffect, useContext } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export function useAuth() {
  return useContext(AuthContext);
}

export function AuthProvider({ children }) {
  const [currentUser, setCurrentUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(true);

  // Configure axios to use the token
  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      localStorage.setItem('token', token);
    } else {
      delete axios.defaults.headers.common['Authorization'];
      localStorage.removeItem('token');
    }
  }, [token]);

  // Load user data when token changes
  useEffect(() => {
    async function loadUser() {
      if (!token) {
        setLoading(false);
        return;
      }

      try {
        const response = await axios.get('/api/user');
        setCurrentUser(response.data);
      } catch (error) {
        console.error('Error loading user:', error);
        // If token is invalid, clear it
        if (error.response && error.response.status === 401) {
          setToken(null);
        }
      } finally {
        setLoading(false);
      }
    }

    loadUser();
  }, [token]);

  // Login function
  const login = async (email, password) => {
    const response = await axios.post('/api/login', { email, password });
    setToken(response.data.access_token);
    setCurrentUser(response.data.user);
    return response.data.user;
  };

  // Register function
  const register = async (userData) => {
    const response = await axios.post('/api/register', userData);
    setToken(response.data.access_token);
    setCurrentUser(response.data.user);
    return response.data.user;
  };

  // Google auth function
  const googleAuth = async (googleData) => {
    const response = await axios.post('/api/google-auth', {
      email: googleData.email,
      name: googleData.name
    });
    setToken(response.data.access_token);
    setCurrentUser(response.data.user);
    return response.data.user;
  };

  // Logout function
  const logout = () => {
    setToken(null);
    setCurrentUser(null);
  };

  // Update user function
  const updateUser = async (userData) => {
    const response = await axios.put('/api/user', userData);
    setCurrentUser(response.data);
    return response.data;
  };

  const value = {
    currentUser,
    loading,
    login,
    register,
    googleAuth,
    logout,
    updateUser,
    isAuthenticated: !!token
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
}
