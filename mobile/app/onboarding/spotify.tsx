import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Image, Linking, Alert } from 'react-native';
import { router } from 'expo-router';
import axios from 'axios';
import Constants from 'expo-constants';

// Define the API URL from environment variables or use a default
const API_URL = Constants.expoConfig?.extra?.apiUrl ?? 'http://localhost:8000';

const SpotifyScreen = () => {
  const [isConnecting, setIsConnecting] = useState(false);

  const handleConnectSpotify = async () => {
    setIsConnecting(true);
    try {
      // Get the authorization URL from the backend
      const response = await axios.get(`${API_URL}/api/v1/playlists/spotify/auth-url`);
      const authUrl = response.data.auth_url;
      
      // Open the Spotify authorization page in the browser
      const supported = await Linking.canOpenURL(authUrl);
      
      if (supported) {
        await Linking.openURL(authUrl);
      } else {
        Alert.alert('Error', 'Cannot open Spotify authorization page');
      }
    } catch (error) {
      console.error('Failed to get Spotify auth URL:', error);
      Alert.alert('Error', 'Failed to connect to Spotify. Please try again later.');
    } finally {
      setIsConnecting(false);
    }
  };

  const handleSkip = () => {
    // Skip Spotify connection and complete onboarding
    // In a real app, you would save all the collected preferences to the backend
    router.replace('/(tabs)' as any);
  };

  const handleFinish = () => {
    // Complete onboarding
    // In a real app, you would save all the collected preferences to the backend
    router.replace('/(tabs)' as any);
  };

  return (
    <View style={styles.container}>
      <View style={styles.content}>
        <Image
          source={require('@/assets/images/spotify-logo.png')}
          style={styles.spotifyLogo}
          resizeMode="contain"
        />
        
        <Text style={styles.title}>Connect with Spotify</Text>
        
        <Text style={styles.description}>
          Link your Spotify account to enjoy personalized music playlists that match your workout intensity and preferences.
        </Text>
        
        <Text style={styles.benefits}>
          • Fresh playlists for every workout{'\n'}
          • Music that matches your exercise intensity{'\n'}
          • Discover new tracks while you sweat
        </Text>
        
        <TouchableOpacity 
          style={styles.connectButton} 
          onPress={handleConnectSpotify}
          disabled={isConnecting}
        >
          <Text style={styles.connectButtonText}>
            {isConnecting ? 'Connecting...' : 'Connect Spotify'}
          </Text>
        </TouchableOpacity>
        
        <TouchableOpacity onPress={handleSkip}>
          <Text style={styles.skipText}>Skip for now</Text>
        </TouchableOpacity>
      </View>
      
      <TouchableOpacity style={styles.finishButton} onPress={handleFinish}>
        <Text style={styles.finishButtonText}>Finish Setup</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
    padding: 20,
    justifyContent: 'space-between',
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  spotifyLogo: {
    width: 120,
    height: 120,
    marginBottom: 30,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#212529',
    marginBottom: 16,
    textAlign: 'center',
  },
  description: {
    fontSize: 16,
    color: '#495057',
    textAlign: 'center',
    marginBottom: 24,
    lineHeight: 24,
  },
  benefits: {
    fontSize: 16,
    color: '#495057',
    marginBottom: 30,
    lineHeight: 24,
    alignSelf: 'flex-start',
    paddingLeft: 20,
  },
  connectButton: {
    backgroundColor: '#1DB954', // Spotify green
    borderRadius: 30,
    paddingVertical: 14,
    paddingHorizontal: 40,
    alignItems: 'center',
    marginBottom: 20,
  },
  connectButtonText: {
    color: 'white',
    fontWeight: 'bold',
    fontSize: 16,
  },
  skipText: {
    fontSize: 16,
    color: '#6c757d',
    textDecorationLine: 'underline',
  },
  finishButton: {
    backgroundColor: '#4361ee',
    borderRadius: 8,
    padding: 16,
    alignItems: 'center',
    marginTop: 20,
  },
  finishButtonText: {
    color: 'white',
    fontWeight: 'bold',
    fontSize: 16,
  },
});

export default SpotifyScreen;
