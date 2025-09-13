import { base44 } from './base44Client';

// Check if we're in development for mock implementations
const isDevelopment = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';

// Create mock implementations for development
const createMockEntities = () => ({
  ThumbnailRequest: {
    create: async (data) => {
      // Mock thumbnail generation
      await new Promise(resolve => setTimeout(resolve, 3000)); // Simulate processing
      return {
        id: 'mock_request_' + Date.now(),
        ...data,
        generated_thumbnail_url: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICA8cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjM0Y0NkZGIi8+CiAgPHRleHQgeD0iNTAlIiB5PSI1MCUiIGZvbnQtZmFtaWx5PSJBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIxOCIgZmlsbD0id2hpdGUiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIj5Nb2NrIFRodW1ibmFpbDwvdGV4dD4KICA8dGV4dCB4PSI1MCUiIHk9IjcwJSIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjE0IiBmaWxsPSIjRkZGRkZGOTAiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIj5HZW5lcmF0ZWQgaW4gRGV2ZWxvcG1lbnQ8L3RleHQ+Cjwvc3ZnPg==',
        status: 'completed',
        created_at: new Date().toISOString()
      };
    }
  },
  
  UsageLimit: {
    filter: async (params) => {
      // Mock usage data - return empty for unlimited usage in development
      return [];
    },
    create: async (data) => {
      // Mock creating usage record
      return {
        id: 'mock_usage_' + Date.now(),
        ...data,
        created_at: new Date().toISOString()
      };
    }
  },
  
  WaitlistUser: base44.entities?.WaitlistUser || {
    create: async (data) => ({
      id: 'mock_waitlist_' + Date.now(),
      ...data,
      created_at: new Date().toISOString()
    })
  }
});

// Export entities - use mock in development if needed, real SDK otherwise
const mockEntities = isDevelopment ? createMockEntities() : null;

export const ThumbnailRequest = isDevelopment ? mockEntities.ThumbnailRequest : base44.entities.ThumbnailRequest;

export const WaitlistUser = isDevelopment ? mockEntities.WaitlistUser : base44.entities.WaitlistUser;

export const UsageLimit = isDevelopment ? mockEntities.UsageLimit : base44.entities.UsageLimit;

// Create mock User entity for development
const createMockUser = () => {
  const mockToken = localStorage.getItem('base44_mock_token');
  const hasMockAuth = mockToken && mockToken.includes('dev_mock_token');
  
  return {
    me: async () => {
      if (!hasMockAuth) {
        throw new Error('Not authenticated');
      }
      // Return mock user data
      return {
        id: 'mock_user_123',
        email: 'developer@localhost.com',
        name: 'Development User',
        created_at: new Date().toISOString()
      };
    },
    redirectToLogin: () => {
      // This should redirect to Django login endpoint
      const loginUrl = `http://127.0.0.1:8000/portfolio/thumbai/login?from_url=${encodeURIComponent(window.location.href)}`;
      window.location.href = loginUrl;
    }
  };
};

// Export User entity - use mock in development, real SDK in production
export const User = isDevelopment ? createMockUser() : base44.auth;