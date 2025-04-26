import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';
import { router } from 'expo-router';

// Define the available equipment options
const EQUIPMENT = [
  { id: 'none', name: 'No Equipment', description: 'Bodyweight exercises only' },
  { id: 'dumbbells', name: 'Dumbbells', description: 'Free weights for resistance training' },
  { id: 'barbell', name: 'Barbell', description: 'For compound movements and heavy lifting' },
  { id: 'kettlebell', name: 'Kettlebell', description: 'For dynamic, full-body movements' },
  { id: 'resistance_bands', name: 'Resistance Bands', description: 'For variable resistance training' },
  { id: 'pullup_bar', name: 'Pull-up Bar', description: 'For upper body and core exercises' },
  { id: 'bench', name: 'Bench', description: 'For various pressing and support exercises' },
  { id: 'gym_access', name: 'Full Gym Access', description: 'Access to all standard gym equipment' },
];

const EquipmentScreen = () => {
  const [selectedEquipment, setSelectedEquipment] = useState<string[]>([]);

  const toggleEquipment = (equipmentId: string) => {
    // If selecting "No Equipment", deselect all others
    if (equipmentId === 'none') {
      if (selectedEquipment.includes('none')) {
        setSelectedEquipment([]);
      } else {
        setSelectedEquipment(['none']);
      }
      return;
    }
    
    // If selecting any other equipment, remove "No Equipment" if it's selected
    let newSelection = [...selectedEquipment];
    if (newSelection.includes('none')) {
      newSelection = newSelection.filter(id => id !== 'none');
    }
    
    // Toggle the selected equipment
    if (newSelection.includes(equipmentId)) {
      newSelection = newSelection.filter(id => id !== equipmentId);
    } else {
      newSelection.push(equipmentId);
    }
    
    setSelectedEquipment(newSelection);
  };

  const handleContinue = () => {
    if (selectedEquipment.length > 0) {
      // In a real app, you would save this selection to context or state management
      router.push('/onboarding/music' as any);
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>What equipment do you have access to?</Text>
        <Text style={styles.subtitle}>This helps us customize exercises for your workouts</Text>
      </View>

      <ScrollView style={styles.scrollView}>
        {EQUIPMENT.map((item) => (
          <TouchableOpacity
            key={item.id}
            style={[
              styles.equipmentCard,
              selectedEquipment.includes(item.id) && styles.selectedEquipmentCard,
            ]}
            onPress={() => toggleEquipment(item.id)}
          >
            <View style={styles.equipmentContent}>
              <Text style={[
                styles.equipmentName,
                selectedEquipment.includes(item.id) && styles.selectedEquipmentName,
              ]}>
                {item.name}
              </Text>
              <Text style={[
                styles.equipmentDescription,
                selectedEquipment.includes(item.id) && styles.selectedEquipmentDescription,
              ]}>
                {item.description}
              </Text>
            </View>
            <View style={[
              styles.checkbox,
              selectedEquipment.includes(item.id) && styles.selectedCheckbox,
            ]}>
              {selectedEquipment.includes(item.id) && <View style={styles.checkboxInner} />}
            </View>
          </TouchableOpacity>
        ))}
      </ScrollView>

      <View style={styles.footer}>
        <Text style={styles.selectionText}>
          {selectedEquipment.length} item{selectedEquipment.length !== 1 ? 's' : ''} selected
        </Text>
        <TouchableOpacity
          style={[styles.button, selectedEquipment.length === 0 && styles.buttonDisabled]}
          onPress={handleContinue}
          disabled={selectedEquipment.length === 0}
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
  equipmentCard: {
    flexDirection: 'row',
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#e9ecef',
  },
  selectedEquipmentCard: {
    borderColor: '#4361ee',
    backgroundColor: '#edf2ff',
  },
  equipmentContent: {
    flex: 1,
  },
  equipmentName: {
    fontSize: 16,
    fontWeight: '500',
    color: '#212529',
    marginBottom: 4,
  },
  selectedEquipmentName: {
    color: '#4361ee',
    fontWeight: 'bold',
  },
  equipmentDescription: {
    fontSize: 14,
    color: '#6c757d',
  },
  selectedEquipmentDescription: {
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

export default EquipmentScreen;
