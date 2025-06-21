import { useAuth } from '@/contexts/AuthContext';
import React from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';

const HomeScreen = () => {
  // Mock data for upcoming workouts
  const upcomingWorkouts = [
    { id: '1', date: 'Today', focus: 'Upper Body', duration: 45 },
    { id: '2', date: 'Tomorrow', focus: 'Lower Body', duration: 60 },
    { id: '3', date: 'Friday', focus: 'Core & Cardio', duration: 30 },
  ];
    const result = useAuth();
    console.log("🚀 ~ HomeScreen ~ result:", result)
  
  // Mock data for workout stats
  const stats = {
    workoutsCompleted: 12,
    totalMinutes: 720,
    streakDays: 5,
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.greeting}>Hello, User!</Text>
        <Text style={styles.subGreeting}>Ready for your next workout?</Text>
      </View>

      <View style={styles.statsContainer}>
        <View style={styles.statItem}>
          <Text style={styles.statNumber}>{stats.workoutsCompleted}</Text>
          <Text style={styles.statLabel}>Workouts</Text>
        </View>
        <View style={styles.statItem}>
          <Text style={styles.statNumber}>{stats.totalMinutes}</Text>
          <Text style={styles.statLabel}>Minutes</Text>
        </View>
        <View style={styles.statItem}>
          <Text style={styles.statNumber}>{stats.streakDays}</Text>
          <Text style={styles.statLabel}>Day Streak</Text>
        </View>
      </View>

      <View style={styles.sectionHeader}>
        <Text style={styles.sectionTitle}>Upcoming Workouts</Text>
        <TouchableOpacity>
          <Text style={styles.seeAllText}>See All</Text>
        </TouchableOpacity>
      </View>

      {upcomingWorkouts.map((workout) => (
        <TouchableOpacity key={workout.id} style={styles.workoutCard}>
          <View style={styles.workoutInfo}>
            <Text style={styles.workoutDate}>{workout.date}</Text>
            <Text style={styles.workoutFocus}>{workout.focus}</Text>
            <Text style={styles.workoutDuration}>{workout.duration} minutes</Text>
          </View>
          <TouchableOpacity style={styles.startButton}>
            <Text style={styles.startButtonText}>Start</Text>
          </TouchableOpacity>
        </TouchableOpacity>
      ))}

      <View style={styles.sectionHeader}>
        <Text style={styles.sectionTitle}>Suggested Playlists</Text>
        <TouchableOpacity>
          <Text style={styles.seeAllText}>See All</Text>
        </TouchableOpacity>
      </View>

      <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.playlistsContainer}>
        <TouchableOpacity style={styles.playlistCard}>
          <View style={styles.playlistImagePlaceholder} />
          <Text style={styles.playlistName}>Workout Mix</Text>
          <Text style={styles.playlistDetails}>15 tracks • 45 min</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.playlistCard}>
          <View style={styles.playlistImagePlaceholder} />
          <Text style={styles.playlistName}>Cardio Boost</Text>
          <Text style={styles.playlistDetails}>12 tracks • 36 min</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.playlistCard}>
          <View style={styles.playlistImagePlaceholder} />
          <Text style={styles.playlistName}>Strength Training</Text>
          <Text style={styles.playlistDetails}>18 tracks • 54 min</Text>
        </TouchableOpacity>
      </ScrollView>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
  },
  header: {
    padding: 20,
    paddingTop: 40,
  },
  greeting: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#212529',
  },
  subGreeting: {
    fontSize: 16,
    color: '#6c757d',
    marginTop: 5,
  },
  statsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    padding: 20,
    backgroundColor: 'white',
    borderRadius: 12,
    marginHorizontal: 20,
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
  statItem: {
    alignItems: 'center',
  },
  statNumber: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#4361ee',
  },
  statLabel: {
    fontSize: 14,
    color: '#6c757d',
    marginTop: 5,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    marginBottom: 10,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#212529',
  },
  seeAllText: {
    fontSize: 14,
    color: '#4361ee',
  },
  workoutCard: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 15,
    marginHorizontal: 20,
    marginBottom: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 1,
  },
  workoutInfo: {
    flex: 1,
  },
  workoutDate: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#4361ee',
    marginBottom: 5,
  },
  workoutFocus: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#212529',
    marginBottom: 5,
  },
  workoutDuration: {
    fontSize: 14,
    color: '#6c757d',
  },
  startButton: {
    backgroundColor: '#4361ee',
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 8,
  },
  startButtonText: {
    color: 'white',
    fontWeight: 'bold',
  },
  playlistsContainer: {
    paddingLeft: 20,
    marginBottom: 20,
  },
  playlistCard: {
    width: 150,
    marginRight: 15,
  },
  playlistImagePlaceholder: {
    width: 150,
    height: 150,
    backgroundColor: '#e9ecef',
    borderRadius: 8,
    marginBottom: 10,
  },
  playlistName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#212529',
    marginBottom: 5,
  },
  playlistDetails: {
    fontSize: 14,
    color: '#6c757d',
  },
});

export default HomeScreen;
