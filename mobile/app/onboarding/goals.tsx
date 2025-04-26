import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';
import { router } from 'expo-router';

// Define the available fitness goals
const GOALS = [
  { id: 'strength', title: 'Build Strength', description: 'Focus on increasing muscle strength and power' },
  { id: 'muscle', title: 'Build Muscle', description: 'Focus on muscle growth and definition' },
  { id: 'endurance', title: 'Improve Endurance', description: 'Focus on stamina and cardiovascular health' },
  { id: 'weight_loss', title: 'Weight Loss', description: 'Focus on burning calories and fat loss' },
  { id: 'toning', title: 'Toning', description: 'Focus on muscle definition without significant size increase' },
  { id: 'flexibility', title: 'Flexibility', description: 'Focus on improving range of motion and flexibility' },
  { id: 'general', title: 'General Fitness', description: 'Balanced approach to overall fitness' },
];

const GoalsScreen = () => {
  const [selectedGoal, setSelectedGoal] = useState<string | null>(null);

  const handleContinue = () => {
    if (selectedGoal) {
      // In a real app, you would save this selection to context or state management
      // For now, we'll just navigate to the next screen
      router.push('/onboarding/level' as any);
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>What's your primary fitness goal?</Text>
        <Text style={styles.subtitle}>This helps us tailor your workout plan</Text>
      </View>

      <ScrollView style={styles.scrollView} showsVerticalScrollIndicator={false}>
        {GOALS.map((goal) => (
          <TouchableOpacity
            key={goal.id}
            style={[
              styles.goalCard,
              selectedGoal === goal.id && styles.selectedGoalCard,
            ]}
            onPress={() => setSelectedGoal(goal.id)}
          >
            <View style={styles.goalContent}>
              <Text style={[
                styles.goalTitle,
                selectedGoal === goal.id && styles.selectedGoalTitle,
              ]}>
                {goal.title}
              </Text>
              <Text style={[
                styles.goalDescription,
                selectedGoal === goal.id && styles.selectedGoalDescription,
              ]}>
                {goal.description}
              </Text>
            </View>
            <View style={[
              styles.checkbox,
              selectedGoal === goal.id && styles.selectedCheckbox,
            ]}>
              {selectedGoal === goal.id && <View style={styles.checkboxInner} />}
            </View>
          </TouchableOpacity>
        ))}
      </ScrollView>

      <TouchableOpacity
        style={[styles.button, !selectedGoal && styles.buttonDisabled]}
        onPress={handleContinue}
        disabled={!selectedGoal}
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
  },
  header: {
    marginBottom: 20,
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
  scrollView: {
    flex: 1,
    marginBottom: 20,
  },
  goalCard: {
    flexDirection: 'row',
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#e9ecef',
  },
  selectedGoalCard: {
    borderColor: '#4361ee',
    backgroundColor: '#edf2ff',
  },
  goalContent: {
    flex: 1,
  },
  goalTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#212529',
    marginBottom: 4,
  },
  selectedGoalTitle: {
    color: '#4361ee',
  },
  goalDescription: {
    fontSize: 14,
    color: '#6c757d',
  },
  selectedGoalDescription: {
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

export default GoalsScreen;
