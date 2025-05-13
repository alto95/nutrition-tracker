import React, { useState } from 'react';
import { Outlet, Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

function MainLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [userMenuOpen, setUserMenuOpen] = useState(false);
  const { currentUser, logout } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  // Generate initials for avatar if no image is available
  const getInitials = () => {
    if (!currentUser || !currentUser.name) return '?';
    return currentUser.name
      .split(' ')
      .map(name => name[0])
      .join('')
      .toUpperCase()
      .substring(0, 2);
  };

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <div
        className={`${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        } fixed z-30 inset-y-0 left-0 w-64 transition duration-300 transform bg-white border-r border-gray-200 md:translate-x-0 md:static md:h-full`}
      >
        <div className="flex items-center justify-between p-4 bg-primary-600">
          <Link to="/" className="text-xl font-bold text-white">Nutrition Tracker</Link>
          <button
            onClick={() => setSidebarOpen(false)}
            className="p-1 rounded-md text-white md:hidden"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <nav className="mt-5 px-2">
          <Link
            to="/"
            className={`group flex items-center px-4 py-2 mb-1 text-sm font-medium rounded-md ${
              location.pathname === '/'
                ? 'bg-gray-200 text-gray-900'
                : 'text-gray-700 hover:bg-gray-100'
            }`}
          >
            <svg
              className={`mr-3 h-5 w-5 ${
                location.pathname === '/' ? 'text-gray-500' : 'text-gray-400'
              }`}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
              />
            </svg>
            Dashboard
          </Link>

          <Link
            to="/meals"
            className={`group flex items-center px-4 py-2 mb-1 text-sm font-medium rounded-md ${
              location.pathname === '/meals'
                ? 'bg-gray-200 text-gray-900'
                : 'text-gray-700 hover:bg-gray-100'
            }`}
          >
            <svg
              className={`mr-3 h-5 w-5 ${
                location.pathname === '/meals' ? 'text-gray-500' : 'text-gray-400'
              }`}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 6v6m0 0v6m0-6h6m-6 0H6"
              />
            </svg>
            Meals
          </Link>

          <Link
            to="/recipes"
            className={`group flex items-center px-4 py-2 mb-1 text-sm font-medium rounded-md ${
              location.pathname === '/recipes'
                ? 'bg-gray-200 text-gray-900'
                : 'text-gray-700 hover:bg-gray-100'
            }`}
          >
            <svg
              className={`mr-3 h-5 w-5 ${
                location.pathname === '/recipes' ? 'text-gray-500' : 'text-gray-400'
              }`}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"
              />
            </svg>
            Recipes
          </Link>

          <Link
            to="/foods"
            className={`group flex items-center px-4 py-2 mb-1 text-sm font-medium rounded-md ${
              location.pathname === '/foods'
                ? 'bg-gray-200 text-gray-900'
                : 'text-gray-700 hover:bg-gray-100'
            }`}
          >
            <svg
              className={`mr-3 h-5 w-5 ${
                location.pathname === '/foods' ? 'text-gray-500' : 'text-gray-400'
              }`}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"
              />
            </svg>
            Foods
          </Link>

          <Link
            to="/glucose"
            className={`group flex items-center px-4 py-2 mb-1 text-sm font-medium rounded-md ${
              location.pathname === '/glucose'
                ? 'bg-gray-200 text-gray-900'
                : 'text-gray-700 hover:bg-gray-100'
            }`}
          >
            <svg
              className={`mr-3 h-5 w-5 ${
                location.pathname === '/glucose' ? 'text-gray-500' : 'text-gray-400'
              }`}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
              />
            </svg>
            Glucose Monitoring
          </Link>

          <Link
            to="/profile"
            className={`group flex items-center px-4 py-2 mb-1 text-sm font-medium rounded-md ${
              location.pathname === '/profile'
                ? 'bg-gray-200 text-gray-900'
                : 'text-gray-700 hover:bg-gray-100'
            }`}
          >
            <svg
              className={`mr-3 h-5 w-5 ${
                location.pathname === '/profile' ? 'text-gray-500' : 'text-gray-400'
              }`}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
              />
            </svg>
            Profile
          </Link>
        </nav>
      </div>

      {/* Content area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="bg-white shadow-sm z-10">
          <div className="flex items-center justify-between px-4 py-3">
            <div className="flex items-center md:hidden">
              <button
                onClick={() => setSidebarOpen(true)}
                className="text-gray-500 hover:text-gray-600"
              >
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M4 6h16M4 12h16M4 18h16"
                  />
                </svg>
              </button>
            </div>

            <div className="flex items-center ml-auto">
              {/* Search */}
              <div className="hidden md:block ml-4">
                <div className="relative flex items-center text-gray-400 focus-within:text-gray-600">
                  <span className="absolute inset-y-0 left-0 flex items-center pl-2">
                    <svg className="w-5 h-5" viewBox="0 0 24 24" fill="none">
                      <path
                        d="M21 21L15 15M17 10C17 13.866 13.866 17 10 17C6.13401 17 3 13.866 3 10C3 6.13401 6.13401 3 10 3C13.866 3 17 6.13401 17 10Z"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      />
                    </svg>
                  </span>
                  <input
                    type="text"
                    className="w-full py-2 pl-10 pr-4 text-sm bg-gray-100 border border-transparent rounded-md focus:outline-none focus:bg-white focus:border-gray-300"
                    placeholder="Search..."
                  />
                </div>
              </div>

              {/* User menu */}
              <div className="ml-4 relative flex-shrink-0">
                <div>
                  <button
                    onClick={() => setUserMenuOpen(!userMenuOpen)}
                    className="flex text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  >
                    <div className="w-8 h-8 rounded-full bg-gray-300 flex items-center justify-center text-gray-700 font-medium">
                      {getInitials()}
                    </div>
                  </button>
                </div>
                {userMenuOpen && (
                  <div className="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5">
                    <div
                      className="py-1"
                      role="menu"
                      aria-orientation="vertical"
                      aria-labelledby="user-menu"
                    >
                      <div className="block px-4 py-2 text-sm text-gray-700 border-b">
                        {currentUser?.name || currentUser?.email}
                      </div>
                      <Link
                        to="/profile"
                        className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                        role="menuitem"
                        onClick={() => setUserMenuOpen(false)}
                      >
                        Your Profile
                      </Link>
                      <button
                        onClick={() => {
                          setUserMenuOpen(false);
                          handleLogout();
                        }}
                        className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                        role="menuitem"
                      >
                        Sign out
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </header>

        {/* Main content */}
        <main className="flex-1 overflow-y-auto p-4 bg-gray-50">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

export default MainLayout;
