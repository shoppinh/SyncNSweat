import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { router } from 'expo-router';

// Define the available fitness levels
const LEVELS = [
  { id: 'beginner', title: 'Beginner', description: 'New to fitness or returning after a long break' },
  { id: 'intermediate', title: 'Intermediate', description: 'Consistent with workouts for several months' },
  { id: 'advanced', title: 'Advanced', description: 'Experienced with various workout routines for years' },
];

const LevelScreen = () => {
  const [selectedLevel, setSelectedLevel] = useState<string | null>(null);

  const handleContinue = () => {
    if (selectedLevel) {
      // In a real app, you would save this selection to context or state management
      router.push('/onboarding/days' as any);
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>What's your fitness level?</Text>
        <Text style={styles.subtitle}>This helps us adjust the intensity of your workouts</Text>
      </View>

      <View style={styles.levelsContainer}>
        {LEVELS.map((level) => (
          <TouchableOpacity
            key={level.id}
            style={[
              styles.levelCard,
              selectedLevel === level.id && styles.selectedLevelCard,
            ]}
            onPress={() => setSelectedLevel(level.id)}
          >
            <View style={styles.levelContent}>
              <Text style={[
                styles.levelTitle,
                selectedLevel === level.id && styles.selectedLevelTitle,
              ]}>
                {level.title}
              </Text>
              <Text style={[
                styles.levelDescription,
                selectedLevel === level.id && styles.selectedLevelDescription,
              ]}>
                {level.description}
              </Text>
            </View>
            <View style={[
              styles.checkbox,
              selectedLevel === level.id && styles.selectedCheckbox,
            ]}>
              {selectedLevel === level.id && <View style={styles.checkboxInner} />}
            </View>
          </TouchableOpacity>
        ))}
      </View>

      <TouchableOpacity
        style={[styles.button, !selectedLevel && styles.buttonDisabled]}
        onPress={handleContinue}
        disabled={!selectedLevel}
      >
        <Text style={styles.buttonText}>Continue</Text>
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
  header: {
    marginBottom: 30,
    marginTop: 10,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#212529',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#6c757d',
  },
  levelsContainer: {
    flex: 1,
  },
  levelCard: {
    flexDirection: 'row',
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 20,
    marginBottom: 16,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#e9ecef',
  },
  selectedLevelCard: {
    borderColor: '#4361ee',
    backgroundColor: '#edf2ff',
  },
  levelContent: {
    flex: 1,
  },
  levelTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#212529',
    marginBottom: 6,
  },
  selectedLevelTitle: {
    color: '#4361ee',
  },
  levelDescription: {
    fontSize: 14,
    color: '#6c757d',
  },
  selectedLevelDescription: {
    color: '#4361ee',
  },
  checkbox: {
    width: 24,
    height: 24,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: '#ced4da',
    marginLeft: 12,
    justifyContent: 'center',
    alignItems: 'center',
  },
  selectedCheckbox: {
    borderColor: '#4361ee',
  },
  checkboxInner: {
    width: 12,
    height: 12,
    borderRadius: 6,
    backgroundColor: '#4361ee',
  },
  button: {
    backgroundColor: '#4361ee',
    borderRadius: 8,
    padding: 16,
    alignItems: 'center',
    marginTop: 20,
  },
  buttonDisabled: {
    backgroundColor: '#adb5bd',
  },
  buttonText: {
    color: 'white',
    fontWeight: 'bold',
    fontSize: 16,
  },
});

export default LevelScreen;
