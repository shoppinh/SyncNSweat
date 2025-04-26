import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';
import { router } from 'expo-router';

// Define the available music genres
const GENRES = [
  { id: 'pop', name: 'Pop' },
  { id: 'rock', name: 'Rock' },
  { id: 'hip_hop', name: 'Hip Hop' },
  { id: 'electronic', name: 'Electronic' },
  { id: 'dance', name: 'Dance' },
  { id: 'r_and_b', name: 'R&B' },
  { id: 'metal', name: 'Metal' },
  { id: 'indie', name: 'Indie' },
  { id: 'classical', name: 'Classical' },
  { id: 'jazz', name: 'Jazz' },
  { id: 'reggae', name: 'Reggae' },
  { id: 'country', name: 'Country' },
];

const MusicScreen = () => {
  const [selectedGenres, setSelectedGenres] = useState<string[]>([]);

  const toggleGenre = (genreId: string) => {
    if (selectedGenres.includes(genreId)) {
      setSelectedGenres(selectedGenres.filter(id => id !== genreId));
    } else if (selectedGenres.length < 5) {
      // Limit to 5 selections
      setSelectedGenres([...selectedGenres, genreId]);
    }
  };

  const handleContinue = () => {
    if (selectedGenres.length > 0) {
      // In a real app, you would save this selection to context or state management
      router.push('/onboarding/spotify' as any);
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>What music do you enjoy while working out?</Text>
        <Text style={styles.subtitle}>Select up to 5 genres you prefer during exercise</Text>
      </View>

      <ScrollView style={styles.scrollView}>
        <View style={styles.genreGrid}>
          {GENRES.map((genre) => (
            <TouchableOpacity
              key={genre.id}
              style={[
                styles.genreCard,
                selectedGenres.includes(genre.id) && styles.selectedGenreCard,
              ]}
              onPress={() => toggleGenre(genre.id)}
              disabled={!selectedGenres.includes(genre.id) && selectedGenres.length >= 5}
            >
              <Text style={[
                styles.genreName,
                selectedGenres.includes(genre.id) && styles.selectedGenreName,
              ]}>
                {genre.name}
              </Text>
            </TouchableOpacity>
          ))}
        </View>
      </ScrollView>

      <View style={styles.footer}>
        <Text style={styles.selectionText}>
          {selectedGenres.length}/5 genres selected
        </Text>
        <TouchableOpacity
          style={[styles.button, selectedGenres.length === 0 && styles.buttonDisabled]}
          onPress={handleContinue}
          disabled={selectedGenres.length === 0}
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
  genreGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  genreCard: {
    width: '48%',
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 1,
    borderColor: '#e9ecef',
    height: 60,
  },
  selectedGenreCard: {
    borderColor: '#4361ee',
    backgroundColor: '#edf2ff',
  },
  genreName: {
    fontSize: 16,
    fontWeight: '500',
    color: '#212529',
  },
  selectedGenreName: {
    color: '#4361ee',
    fontWeight: 'bold',
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

export default MusicScreen;
