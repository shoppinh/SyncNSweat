import React from 'react';
import { View, Text, StyleSheet, Image, TouchableOpacity } from 'react-native';
import { router } from 'expo-router';

const WelcomeScreen = () => {
  const handleContinue = () => {
    router.push('/onboarding/goals');
  };

  return (
    <View style={styles.container}>
      <View style={styles.content}>
        <Image
          source={require('@/assets/images/welcome-illustration.png')}
          style={styles.image}
          resizeMode="contain"
        />
        
        <Text style={styles.title}>Welcome to Sync & Sweat</Text>
        
        <Text style={styles.description}>
          Your personalized fitness companion that keeps your workouts fresh and your music exciting.
        </Text>
        
        <Text style={styles.subtitle}>
          Let's get to know you better to create your perfect workout experience.
        </Text>
      </View>
      
      <TouchableOpacity style={styles.button} onPress={handleContinue}>
        <Text style={styles.buttonText}>Get Started</Text>
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
  image: {
    width: '80%',
    height: 200,
    marginBottom: 30,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#212529',
    marginBottom: 20,
    textAlign: 'center',
  },
  description: {
    fontSize: 16,
    color: '#495057',
    textAlign: 'center',
    marginBottom: 20,
    lineHeight: 24,
  },
  subtitle: {
    fontSize: 16,
    color: '#6c757d',
    textAlign: 'center',
    lineHeight: 24,
  },
  button: {
    backgroundColor: '#4361ee',
    borderRadius: 8,
    padding: 16,
    alignItems: 'center',
    marginTop: 20,
  },
  buttonText: {
    color: 'white',
    fontWeight: 'bold',
    fontSize: 16,
  },
});

export default WelcomeScreen;
