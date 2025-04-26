import React, { createContext, useState, useContext, ReactNode, useMemo, useCallback } from 'react';
import axios from 'axios';
import Constants from 'expo-constants';
import { router } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Define the API URL from environment variables or use a default
const API_URL = Constants.expoConfig?.extra?.apiUrl ?? 'http://localhost:8000';

// Define the shape of our user preferences
interface UserPreferences {
  goal: string | null;
  fitnessLevel: string | null;
  availableDays: string[];
  equipment: string[];
  musicGenres: string[];
  spotifyConnected: boolean;
}

// Define the shape of our onboarding context
interface OnboardingContextType {
  preferences: UserPreferences;
  isLoading: boolean;
  error: string | null;
  setGoal: (goal: string) => void;
  setFitnessLevel: (level: string) => void;
  setAvailableDays: (days: string[]) => void;
  setEquipment: (equipment: string[]) => void;
  setMusicGenres: (genres: string[]) => void;
  setSpotifyConnected: (connected: boolean) => void;
  savePreferences: () => Promise<void>;
  clearError: () => void;
}

// Create the context with a default value
const OnboardingContext = createContext<OnboardingContextType>({
  preferences: {
    goal: null,
    fitnessLevel: null,
    availableDays: [],
    equipment: [],
    musicGenres: [],
    spotifyConnected: false,
  },
  isLoading: false,
  error: null,
  setGoal: () => {},
  setFitnessLevel: () => {},
  setAvailableDays: () => {},
  setEquipment: () => {},
  setMusicGenres: () => {},
  setSpotifyConnected: () => {},
  savePreferences: async () => {},
  clearError: () => {},
});

// Create a provider component
export const OnboardingProvider = ({ children }: { children: ReactNode }) => {
  const [preferences, setPreferences] = useState<UserPreferences>({
    goal: null,
    fitnessLevel: null,
    availableDays: [],
    equipment: [],
    musicGenres: [],
    spotifyConnected: false,
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Update functions for each preference - wrapped in useCallback to prevent unnecessary re-renders
  const setGoal = useCallback((goal: string) => {
    setPreferences(prev => ({ ...prev, goal }));
  }, []);

  const setFitnessLevel = useCallback((fitnessLevel: string) => {
    setPreferences(prev => ({ ...prev, fitnessLevel }));
  }, []);

  const setAvailableDays = useCallback((availableDays: string[]) => {
    setPreferences(prev => ({ ...prev, availableDays }));
  }, []);

  const setEquipment = useCallback((equipment: string[]) => {
    setPreferences(prev => ({ ...prev, equipment }));
  }, []);

  const setMusicGenres = useCallback((musicGenres: string[]) => {
    setPreferences(prev => ({ ...prev, musicGenres }));
  }, []);

  const setSpotifyConnected = useCallback((spotifyConnected: boolean) => {
    setPreferences(prev => ({ ...prev, spotifyConnected }));
  }, []);

  // Clear error function
  const clearError = useCallback(() => {
    setError(null);
  }, []);

  // Save preferences to the backend - wrapped in useCallback to prevent unnecessary re-renders
  const savePreferences = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      // Make the API request to save preferences
      await axios.put(`${API_URL}/api/v1/profiles/me/preferences`, preferences, {
        headers: {
          'Content-Type': 'application/json',
          // Include authorization header if needed
          // 'Authorization': `Bearer ${token}`
        },
      });
      
      // Mark onboarding as completed in AsyncStorage
      await AsyncStorage.setItem('onboardingCompleted', 'true');
      
      // Navigate to the main app after successful save
      router.replace('/(tabs)' as any);
    } catch (error: any) {
      console.error('Failed to save preferences:', error);
      
      if (error.response) {
        setError(error.response.data.detail || 'Failed to save preferences. Please try again.');
      } else if (error.request) {
        setError('No response from server. Please check your internet connection.');
      } else {
        setError('An unexpected error occurred. Please try again later.');
      }
    } finally {
      setIsLoading(false);
    }
  }, [preferences]);

  // Memoize the context value to prevent unnecessary re-renders
  const contextValue = useMemo(() => ({
    preferences,
    isLoading,
    error,
    setGoal,
    setFitnessLevel,
    setAvailableDays,
    setEquipment,
    setMusicGenres,
    setSpotifyConnected,
    savePreferences,
    clearError,
  }), [
    preferences,
    isLoading,
    error,
    setGoal,
    setFitnessLevel,
    setAvailableDays,
    setEquipment,
    setMusicGenres,
    setSpotifyConnected,
    savePreferences,
    clearError,
  ]);

  return (
    <OnboardingContext.Provider value={contextValue}>
      {children}
    </OnboardingContext.Provider>
  );
};

// Create a hook to use the onboarding context
export const useOnboarding = () => useContext(OnboardingContext);

export default OnboardingContext;
