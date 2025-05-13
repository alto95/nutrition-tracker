import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

// Import contexts
import { AuthProvider } from './contexts/AuthContext';

// Import layouts
import MainLayout from './layouts/MainLayout';

// Import pages
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Profile from './pages/Profile';
import Meals from './pages/Meals';
import Recipes from './pages/Recipes';
import Foods from './pages/Foods';
import Glucose from './pages/Glucose';
import NotFound from './pages/NotFound';

// Import guards
import PrivateRoute from './components/PrivateRoute';

function App() {
  return (
    <AuthProvider>
      <Router>
        <ToastContainer position="top-right" autoClose={3000} />
        <Routes>
          {/* Public routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          
          {/* Private routes */}
          <Route path="/" element={<PrivateRoute><MainLayout /></PrivateRoute>}>
            <Route index element={<Home />} />
            <Route path="profile" element={<Profile />} />
            <Route path="meals" element={<Meals />} />
            <Route path="recipes" element={<Recipes />} />
            <Route path="foods" element={<Foods />} />
            <Route path="glucose" element={<Glucose />} />
          </Route>
          
          {/* Not found route */}
          <Route path="404" element={<NotFound />} />
          <Route path="*" element={<Navigate to="/404" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
