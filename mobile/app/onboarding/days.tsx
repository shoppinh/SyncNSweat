import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';
import { router } from 'expo-router';

// Define the days of the week
const DAYS = [
  { id: 'monday', name: 'Monday' },
  { id: 'tuesday', name: 'Tuesday' },
  { id: 'wednesday', name: 'Wednesday' },
  { id: 'thursday', name: 'Thursday' },
  { id: 'friday', name: 'Friday' },
  { id: 'saturday', name: 'Saturday' },
  { id: 'sunday', name: 'Sunday' },
];

const DaysScreen = () => {
  const [selectedDays, setSelectedDays] = useState<string[]>([]);

  const toggleDay = (dayId: string) => {
    if (selectedDays.includes(dayId)) {
      setSelectedDays(selectedDays.filter(id => id !== dayId));
    } else {
      setSelectedDays([...selectedDays, dayId]);
    }
  };

  const handleContinue = () => {
    if (selectedDays.length > 0) {
      // In a real app, you would save this selection to context or state management
      router.push('/onboarding/equipment' as any);
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Which days can you work out?</Text>
        <Text style={styles.subtitle}>Select all days you're available for exercise</Text>
      </View>

      <ScrollView style={styles.scrollView}>
        {DAYS.map((day) => (
          <TouchableOpacity
            key={day.id}
            style={[
              styles.dayCard,
              selectedDays.includes(day.id) && styles.selectedDayCard,
            ]}
            onPress={() => toggleDay(day.id)}
          >
            <Text style={[
              styles.dayName,
              selectedDays.includes(day.id) && styles.selectedDayName,
            ]}>
              {day.name}
            </Text>
            <View style={[
              styles.checkbox,
              selectedDays.includes(day.id) && styles.selectedCheckbox,
            ]}>
              {selectedDays.includes(day.id) && <View style={styles.checkboxInner} />}
            </View>
          </TouchableOpacity>
        ))}
      </ScrollView>

      <View style={styles.footer}>
        <Text style={styles.selectionText}>
          {selectedDays.length} day{selectedDays.length !== 1 ? 's' : ''} selected
        </Text>
        <TouchableOpacity
          style={[styles.button, selectedDays.length === 0 && styles.buttonDisabled]}
          onPress={handleContinue}
          disabled={selectedDays.length === 0}
        >
          <Text style={styles.buttonText}>Continue</Text>
        </TouchableOpacity>
      </View>
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
  },
  dayCard: {
    flexDirection: 'row',
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    alignItems: 'center',
    justifyContent: 'space-between',
    borderWidth: 1,
    borderColor: '#e9ecef',
  },
  selectedDayCard: {
    borderColor: '#4361ee',
    backgroundColor: '#edf2ff',
  },
  dayName: {
    fontSize: 16,
    fontWeight: '500',
    color: '#212529',
  },
  selectedDayName: {
    color: '#4361ee',
    fontWeight: 'bold',
  },
  checkbox: {
    width: 24,
    height: 24,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: '#ced4da',
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
  footer: {
    marginTop: 20,
  },
  selectionText: {
    fontSize: 14,
    color: '#6c757d',
    textAlign: 'center',
    marginBottom: 12,
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

export default DaysScreen;
