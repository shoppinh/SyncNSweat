import React, { useState } from "react";
import {
  FlatList,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";

interface WorkoutItem {
  date: string;
  focus: string;
  duration: number;
  completed: boolean;
  exercises: Exercise[];
}

interface Exercise {
  id: string;
  name: string;
  sets: number;
  reps: string;
  completed: boolean;
}

const WorkoutScreen = () => {
  // Mock data for workouts
  const [workouts, setWorkouts] = useState([
    {
      id: "1",
      date: "2023-11-15",
      focus: "Upper Body",
      duration: 45,
      completed: true,
      exercises: [
        {
          id: "1-1",
          name: "Bench Press",
          sets: 3,
          reps: "8-10",
          completed: true,
        },
        { id: "1-2", name: "Pull-ups", sets: 3, reps: "8-10", completed: true },
        {
          id: "1-3",
          name: "Shoulder Press",
          sets: 3,
          reps: "8-10",
          completed: true,
        },
      ],
    },
    {
      id: "2",
      date: "2023-11-17",
      focus: "Lower Body",
      duration: 60,
      completed: false,
      exercises: [
        { id: "2-1", name: "Squats", sets: 4, reps: "10-12", completed: false },
        {
          id: "2-2",
          name: "Deadlifts",
          sets: 4,
          reps: "8-10",
          completed: false,
        },
        { id: "2-3", name: "Lunges", sets: 3, reps: "12-15", completed: false },
        {
          id: "2-4",
          name: "Calf Raises",
          sets: 3,
          reps: "15-20",
          completed: false,
        },
      ],
    },
    {
      id: "3",
      date: "2023-11-19",
      focus: "Core & Cardio",
      duration: 30,
      completed: false,
      exercises: [
        { id: "3-1", name: "Plank", sets: 3, reps: "60 sec", completed: false },
        {
          id: "3-2",
          name: "Russian Twists",
          sets: 3,
          reps: "20",
          completed: false,
        },
        {
          id: "3-3",
          name: "Mountain Climbers",
          sets: 3,
          reps: "30 sec",
          completed: false,
        },
        { id: "3-4", name: "Burpees", sets: 3, reps: "10", completed: false },
      ],
    },
  ]);

  const [activeTab, setActiveTab] = useState("upcoming");

  const upcomingWorkouts = workouts.filter((workout) => !workout.completed);
  const completedWorkouts = workouts.filter((workout) => workout.completed);

  const renderWorkoutItem = ({ item }: { item: WorkoutItem }) => (
    <TouchableOpacity style={styles.workoutCard}>
      <View style={styles.workoutHeader}>
        <Text style={styles.workoutDate}>
          {new Date(item.date).toLocaleDateString("en-US", {
            weekday: "long",
            month: "short",
            day: "numeric",
          })}
        </Text>
        <Text style={styles.workoutDuration}>{item.duration} min</Text>
      </View>
      <Text style={styles.workoutFocus}>{item.focus}</Text>

      <View style={styles.exercisesList}>
        {item.exercises.map((exercise) => (
          <View key={exercise.id} style={styles.exerciseItem}>
            <Text style={styles.exerciseName}>{exercise.name}</Text>
            <Text style={styles.exerciseDetails}>
              {exercise.sets} sets × {exercise.reps}
            </Text>
          </View>
        ))}
      </View>

      <TouchableOpacity
        style={[
          styles.actionButton,
          item.completed ? styles.viewDetailsButton : styles.startWorkoutButton,
        ]}
      >
        <Text style={styles.actionButtonText}>
          {item.completed ? "View Details" : "Start Workout"}
        </Text>
      </TouchableOpacity>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Workouts</Text>
      </View>

      <View style={styles.tabContainer}>
        <TouchableOpacity
          style={[styles.tab, activeTab === "upcoming" && styles.activeTab]}
          onPress={() => setActiveTab("upcoming")}
        >
          <Text
            style={[
              styles.tabText,
              activeTab === "upcoming" && styles.activeTabText,
            ]}
          >
            Upcoming
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.tab, activeTab === "completed" && styles.activeTab]}
          onPress={() => setActiveTab("completed")}
        >
          <Text
            style={[
              styles.tabText,
              activeTab === "completed" && styles.activeTabText,
            ]}
          >
            Completed
          </Text>
        </TouchableOpacity>
      </View>

      <FlatList
        data={activeTab === "upcoming" ? upcomingWorkouts : completedWorkouts}
        renderItem={renderWorkoutItem}
        keyExtractor={(item) => item.id}
        contentContainerStyle={styles.listContainer}
        showsVerticalScrollIndicator={false}
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Text style={styles.emptyText}>
              {activeTab === "upcoming"
                ? "No upcoming workouts. Create a new workout plan!"
                : "No completed workouts yet. Start working out!"}
            </Text>
          </View>
        }
      />

      <TouchableOpacity style={styles.floatingButton}>
        <Text style={styles.floatingButtonText}>+</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#f8f9fa",
  },
  header: {
    padding: 20,
    paddingTop: 40,
    backgroundColor: "white",
  },
  title: {
    fontSize: 28,
    fontWeight: "bold",
    color: "#212529",
  },
  tabContainer: {
    flexDirection: "row",
    backgroundColor: "white",
    paddingHorizontal: 20,
    paddingBottom: 15,
  },
  tab: {
    marginRight: 20,
    paddingBottom: 5,
  },
  activeTab: {
    borderBottomWidth: 2,
    borderBottomColor: "#4361ee",
  },
  tabText: {
    fontSize: 16,
    color: "#6c757d",
  },
  activeTabText: {
    color: "#4361ee",
    fontWeight: "bold",
  },
  listContainer: {
    padding: 20,
    paddingBottom: 80, // Extra padding for the floating button
  },
  workoutCard: {
    backgroundColor: "white",
    borderRadius: 12,
    padding: 15,
    marginBottom: 15,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 1,
  },
  workoutHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginBottom: 5,
  },
  workoutDate: {
    fontSize: 14,
    color: "#4361ee",
    fontWeight: "bold",
  },
  workoutDuration: {
    fontSize: 14,
    color: "#6c757d",
  },
  workoutFocus: {
    fontSize: 18,
    fontWeight: "bold",
    color: "#212529",
    marginBottom: 10,
  },
  exercisesList: {
    marginBottom: 15,
  },
  exerciseItem: {
    flexDirection: "row",
    justifyContent: "space-between",
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: "#e9ecef",
  },
  exerciseName: {
    fontSize: 16,
    color: "#212529",
  },
  exerciseDetails: {
    fontSize: 14,
    color: "#6c757d",
  },
  actionButton: {
    borderRadius: 8,
    padding: 12,
    alignItems: "center",
  },
  startWorkoutButton: {
    backgroundColor: "#4361ee",
  },
  viewDetailsButton: {
    backgroundColor: "#e9ecef",
  },
  actionButtonText: {
    fontWeight: "bold",
    fontSize: 16,
    color: "white",
  },
  emptyContainer: {
    alignItems: "center",
    justifyContent: "center",
    padding: 20,
  },
  emptyText: {
    fontSize: 16,
    color: "#6c757d",
    textAlign: "center",
  },
  floatingButton: {
    position: "absolute",
    bottom: 20,
    right: 20,
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: "#4361ee",
    justifyContent: "center",
    alignItems: "center",
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 4,
    elevation: 4,
  },
  floatingButtonText: {
    fontSize: 30,
    color: "white",
  },
});

export default WorkoutScreen;
