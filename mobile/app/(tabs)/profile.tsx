import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView, Switch } from 'react-native';

const ProfileScreen = () => {
  // Mock user data
  const user = {
    name: 'John Doe',
    email: 'john.doe@example.com',
    fitnessGoal: 'Strength',
    fitnessLevel: 'Intermediate',
    availableDays: ['Monday', 'Wednesday', 'Friday'],
    workoutDuration: 60,
  };

  // Mock preferences
  const preferences = {
    availableEquipment: ['Dumbbells', 'Barbell', 'Bench'],
    musicGenres: ['Rock', 'Hip Hop', 'Electronic'],
    musicTempo: 'Medium',
    targetMuscleGroups: ['Chest', 'Back', 'Legs'],
    spotifyConnected: true,
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <View style={styles.profileImagePlaceholder}>
          <Text style={styles.profileInitials}>{user.name.charAt(0)}</Text>
        </View>
        <Text style={styles.userName}>{user.name}</Text>
        <Text style={styles.userEmail}>{user.email}</Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Fitness Profile</Text>
        <View style={styles.card}>
          <View style={styles.row}>
            <Text style={styles.label}>Fitness Goal</Text>
            <Text style={styles.value}>{user.fitnessGoal}</Text>
          </View>
          <View style={styles.divider} />
          <View style={styles.row}>
            <Text style={styles.label}>Fitness Level</Text>
            <Text style={styles.value}>{user.fitnessLevel}</Text>
          </View>
          <View style={styles.divider} />
          <View style={styles.row}>
            <Text style={styles.label}>Available Days</Text>
            <Text style={styles.value}>{user.availableDays.join(', ')}</Text>
          </View>
          <View style={styles.divider} />
          <View style={styles.row}>
            <Text style={styles.label}>Workout Duration</Text>
            <Text style={styles.value}>{user.workoutDuration} minutes</Text>
          </View>
        </View>
        <TouchableOpacity style={styles.editButton}>
          <Text style={styles.editButtonText}>Edit Fitness Profile</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Preferences</Text>
        <View style={styles.card}>
          <View style={styles.row}>
            <Text style={styles.label}>Available Equipment</Text>
            <Text style={styles.value}>{preferences.availableEquipment.join(', ')}</Text>
          </View>
          <View style={styles.divider} />
          <View style={styles.row}>
            <Text style={styles.label}>Music Genres</Text>
            <Text style={styles.value}>{preferences.musicGenres.join(', ')}</Text>
          </View>
          <View style={styles.divider} />
          <View style={styles.row}>
            <Text style={styles.label}>Music Tempo</Text>
            <Text style={styles.value}>{preferences.musicTempo}</Text>
          </View>
          <View style={styles.divider} />
          <View style={styles.row}>
            <Text style={styles.label}>Target Muscle Groups</Text>
            <Text style={styles.value}>{preferences.targetMuscleGroups.join(', ')}</Text>
          </View>
        </View>
        <TouchableOpacity style={styles.editButton}>
          <Text style={styles.editButtonText}>Edit Preferences</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Integrations</Text>
        <View style={styles.card}>
          <View style={styles.row}>
            <Text style={styles.label}>Spotify</Text>
            <Switch
              value={preferences.spotifyConnected}
              trackColor={{ false: '#e9ecef', true: '#4361ee' }}
              thumbColor={'#ffffff'}
            />
          </View>
        </View>
      </View>

      <TouchableOpacity style={styles.logoutButton}>
        <Text style={styles.logoutButtonText}>Log Out</Text>
      </TouchableOpacity>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
  },
  header: {
    alignItems: 'center',
    padding: 20,
    paddingTop: 40,
    backgroundColor: 'white',
  },
  profileImagePlaceholder: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: '#4361ee',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 15,
  },
  profileInitials: {
    fontSize: 40,
    fontWeight: 'bold',
    color: 'white',
  },
  userName: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#212529',
    marginBottom: 5,
  },
  userEmail: {
    fontSize: 16,
    color: '#6c757d',
  },
  section: {
    padding: 20,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#212529',
    marginBottom: 15,
  },
  card: {
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 1,
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 10,
  },
  label: {
    fontSize: 16,
    color: '#212529',
  },
  value: {
    fontSize: 16,
    color: '#6c757d',
    maxWidth: '60%',
    textAlign: 'right',
  },
  divider: {
    height: 1,
    backgroundColor: '#e9ecef',
  },
  editButton: {
    marginTop: 15,
    alignSelf: 'flex-end',
  },
  editButtonText: {
    fontSize: 16,
    color: '#4361ee',
    fontWeight: 'bold',
  },
  logoutButton: {
    margin: 20,
    backgroundColor: '#f8d7da',
    borderRadius: 8,
    padding: 15,
    alignItems: 'center',
  },
  logoutButtonText: {
    color: '#dc3545',
    fontWeight: 'bold',
    fontSize: 16,
  },
});

export default ProfileScreen;
