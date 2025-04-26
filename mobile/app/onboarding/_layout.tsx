import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { usePathname, useRouter, Stack } from 'expo-router';

// Define the onboarding steps
const ONBOARDING_STEPS = [
  { id: 'index', title: 'Welcome' },
  { id: 'goals', title: 'Goals' },
  { id: 'level', title: 'Fitness Level' },
  { id: 'days', title: 'Available Days' },
  { id: 'equipment', title: 'Equipment' },
  { id: 'music', title: 'Music Preferences' },
  { id: 'spotify', title: 'Connect Spotify' },
];

export default function OnboardingLayout() {
  const pathname = usePathname();
  const router = useRouter();
  
  // Extract the current step from the pathname
  const currentStepId = pathname.split('/').pop() || 'index';
  const currentStepIndex = ONBOARDING_STEPS.findIndex(step => step.id === currentStepId);
  
  // Calculate progress percentage
  const progress = ((currentStepIndex + 1) / ONBOARDING_STEPS.length) * 100;
  
  const handleSkip = () => {
    // Skip to the main app
    router.replace('/(tabs)');
  };
  
  return (
    <View style={styles.container}>
      {/* Progress indicator */}
      <View style={styles.progressContainer}>
        <View style={[styles.progressBar, { width: `${progress}%` }]} />
      </View>
      
      {/* Step indicator */}
      <View style={styles.stepIndicator}>
        <Text style={styles.stepText}>
          Step {currentStepIndex + 1} of {ONBOARDING_STEPS.length}
        </Text>
        <TouchableOpacity onPress={handleSkip}>
          <Text style={styles.skipText}>Skip</Text>
        </TouchableOpacity>
      </View>
      
      {/* Stack navigator for onboarding screens */}
      <Stack screenOptions={{
        headerShown: false,
        animation: 'slide_from_right',
      }} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
  },
  progressContainer: {
    height: 4,
    backgroundColor: '#e9ecef',
    width: '100%',
  },
  progressBar: {
    height: '100%',
    backgroundColor: '#4361ee',
  },
  stepIndicator: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    paddingVertical: 10,
  },
  stepText: {
    fontSize: 14,
    color: '#6c757d',
  },
  skipText: {
    fontSize: 14,
    color: '#4361ee',
    fontWeight: '500',
  },
});
