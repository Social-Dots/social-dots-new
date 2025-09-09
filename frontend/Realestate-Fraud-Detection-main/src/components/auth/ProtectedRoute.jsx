import React from 'react';
import { useAuth } from '@/contexts/AuthContext';
import Login from './Login';

/**
 * ProtectedRoute Component
 * 
 * Provides route-level authentication protection. Shows a loading state while
 * checking authentication, renders the login form for unauthenticated users,
 * and displays the protected content for authenticated users.
 * 
 * @param {ReactNode} children - The protected content to render when authenticated
 * @returns {JSX.Element} Loading state, login form, or protected content
 */
export default function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuth();

  // Show loading state while authentication is being verified
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-red-50 via-white to-red-50">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-red-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  // Show login form if user is not authenticated
  if (!isAuthenticated) {
    return <Login />;
  }

  // Render protected content if user is authenticated
  return children;
}