import React, { createContext, useState, useContext, ReactNode, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { router } from 'expo-router';
import axios from 'axios';
import Constants from 'expo-constants';

// Define the API URL from environment variables or use a default
const API_URL = Constants.expoConfig?.extra?.apiUrl || 'http://localhost:8000';

// Define the shape of our authentication context
interface AuthContextType {
  isAuthenticated: boolean;
  user: any | null;
  token: string | null;
  isLoading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  signup: (email: string, password: string, name: string) => Promise<void>;
  clearError: () => void;
}

// Create the context with a default value
const AuthContext = createContext<AuthContextType>({
  isAuthenticated: false,
  user: null,
  token: null,
  isLoading: false,
  error: null,
  login: async () => {},
  logout: async () => {},
  signup: async () => {},
  clearError: () => {},
});

// Storage keys
const TOKEN_KEY = 'auth_token';
const USER_KEY = 'user_data';

// Create a provider component
export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<any | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Initialize auth state from storage
  useEffect(() => {
    const loadAuthState = async () => {
      try {
        const storedToken = await AsyncStorage.getItem(TOKEN_KEY);
        const storedUser = await AsyncStorage.getItem(USER_KEY);
        
        if (storedToken && storedUser) {
          setToken(storedToken);
          setUser(JSON.parse(storedUser));
          setIsAuthenticated(true);
          
          // Set the default Authorization header for all requests
          axios.defaults.headers.common['Authorization'] = `Bearer ${storedToken}`;
        }
      } catch (error) {
        console.error('Failed to load auth state:', error);
      } finally {
        setIsLoading(false);
      }
    };
    
    loadAuthState();
  }, []);

  // Save auth state to storage
  const saveAuthState = async (newToken: string, newUser: any) => {
    try {
      await AsyncStorage.setItem(TOKEN_KEY, newToken);
      await AsyncStorage.setItem(USER_KEY, JSON.stringify(newUser));
    } catch (error) {
      console.error('Failed to save auth state:', error);
    }
  };

  // Clear auth state from storage
  const clearAuthState = async () => {
    try {
      await AsyncStorage.removeItem(TOKEN_KEY);
      await AsyncStorage.removeItem(USER_KEY);
    } catch (error) {
      console.error('Failed to clear auth state:', error);
    }
  };

  // Login function
  const login = async (email: string, password: string) => {
    setIsLoading(true);
    setError(null);
    
    try {
      // Create form data for OAuth2 password flow
      const formData = new FormData();
      formData.append('username', email);
      formData.append('password', password);
      
      // Make the login request
      const response = await axios.post(`${API_URL}/api/v1/auth/login`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      const { access_token, token_type } = response.data;
      
      // Set the token in axios defaults
      axios.defaults.headers.common['Authorization'] = `${token_type} ${access_token}`;
      
      // Get user info
      const userResponse = await axios.get(`${API_URL}/api/v1/auth/me`);
      const userData = userResponse.data;
      
      // Update state
      setToken(access_token);
      setUser(userData);
      setIsAuthenticated(true);
      
      // Save to storage
      await saveAuthState(access_token, userData);
      
      // Navigate to the main app
      router.replace('/(tabs)/');
    } catch (error: any) {
      console.error('Login error:', error);
      
      if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        setError(error.response.data.detail || 'Login failed. Please check your credentials.');
      } else if (error.request) {
        // The request was made but no response was received
        setError('No response from server. Please check your internet connection.');
      } else {
        // Something happened in setting up the request that triggered an Error
        setError('An unexpected error occurred. Please try again later.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  // Logout function
  const logout = async () => {
    setIsLoading(true);
    
    try {
      // Clear auth state from storage
      await clearAuthState();
      
      // Clear axios default headers
      delete axios.defaults.headers.common['Authorization'];
      
      // Update state
      setToken(null);
      setUser(null);
      setIsAuthenticated(false);
      
      // Navigate to login screen
      router.replace('/');
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // Signup function
  const signup = async (email: string, password: string, name: string) => {
    setIsLoading(true);
    setError(null);
    
    try {
      // Make the signup request
      const response = await axios.post(`${API_URL}/api/v1/auth/register`, {
        email,
        password,
        name,
      });
      
      // After successful signup, log the user in
      await login(email, password);
    } catch (error: any) {
      console.error('Signup error:', error);
      
      if (error.response) {
        setError(error.response.data.detail || 'Signup failed. Please try again.');
      } else if (error.request) {
        setError('No response from server. Please check your internet connection.');
      } else {
        setError('An unexpected error occurred. Please try again later.');
      }
      
      setIsLoading(false);
    }
  };

  // Clear error function
  const clearError = () => {
    setError(null);
  };

  // Provide the auth context to children components
  return (
    <AuthContext.Provider
      value={{
        isAuthenticated,
        user,
        token,
        isLoading,
        error,
        login,
        logout,
        signup,
        clearError,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

// Create a hook to use the auth context
export const useAuth = () => useContext(AuthContext);

export default AuthContext;
