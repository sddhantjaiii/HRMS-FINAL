// API Configuration for different environments
export const API_CONFIG = {
  // Automatically detect environment
  getBaseUrl: () => {
    // Check for environment variables first
    const backendUrl = import.meta.env.VITE_BACKEND_URL;
    if (backendUrl) {
      return backendUrl;
    }

    // For Vercel deployment or other production environments
    if (import.meta.env.PROD) {
      // In production, use the same domain with HTTPS
      const protocol = window.location.protocol;
      return `${protocol}//${window.location.hostname}`;
    }

    // For localhost/development
    if (
      window.location.hostname === "localhost" ||
      window.location.hostname === "127.0.0.1"
    ) {
      return "http://127.0.0.1:8000";
    }

    // For any other domain, use the current domain with appropriate protocol
    const protocol = window.location.protocol;
    return `${protocol}//${window.location.hostname}`;
  },

  // Get the full API URL
  getApiUrl: (endpoint: string = "") => {
    const baseUrl = API_CONFIG.getBaseUrl();
    return `${baseUrl}/api${endpoint}`;
  },
};

// Export the base URL for backward compatibility
export const API_BASE_URL = API_CONFIG.getBaseUrl();
export const API_BASE = API_CONFIG.getApiUrl();
