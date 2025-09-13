import { createClient } from '@base44/sdk';

// Check if we're in development and have a mock token
const isDevelopment = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
const urlParams = new URLSearchParams(window.location.search);
const mockToken = urlParams.get('access_token');

// For development, simulate a successful authentication
let clientConfig = {
  appId: "6883d8876847402fc656950d",
  requiresAuth: false
};

// Enhanced mock token handling for development
if (isDevelopment && mockToken && mockToken.includes('dev_mock_token')) {
  clientConfig.token = mockToken;
  clientConfig.requiresAuth = true; // Enable auth features with mock token
  
  // Store token in localStorage for persistence across page refreshes
  if (typeof window !== 'undefined' && window.localStorage) {
    localStorage.setItem('base44_mock_token', mockToken);
  }
  
  // Clean the URL to remove the token parameter for security
  if (window.history && window.history.replaceState) {
    const url = new URL(window.location);
    url.searchParams.delete('access_token');
    window.history.replaceState({}, '', url);
  }
} else if (isDevelopment) {
  // Check for stored mock token
  const storedMockToken = localStorage.getItem('base44_mock_token');
  if (storedMockToken && storedMockToken.includes('dev_mock_token')) {
    clientConfig.token = storedMockToken;
    clientConfig.requiresAuth = true;
  }
}

// Create a client with the configuration
export const base44 = createClient(clientConfig);
