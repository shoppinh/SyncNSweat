import unittest
from unittest.mock import patch, MagicMock
import json
import os
import sys

# Add the parent directory to the path so we can import the app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.exercise import ExerciseService
from app.core.config import settings

class TestExerciseService(unittest.TestCase):
    # Have to import db session
    def setUp(self):
        self.exercise_service = ExerciseService()
    
    @patch('requests.get')
    def test_get_exercises_from_external_source(self, mock_get):
        # Mock the response from the Exercise API
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {
                "id": "0001",
                "name": "Barbell Bench Press",
                "target": "pectorals",
                "equipment": "barbell"
            },
            {
                "id": "0002",
                "name": "Push-up",
                "target": "pectorals",
                "equipment": "body weight"
            }
        ]
        mock_get.return_value = mock_response
        
        # Call the method
        result = self.exercise_service.get_exercises_from_external_source()
        
        # Check the result
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "0001")
        self.assertEqual(result[0]["name"], "Barbell Bench Press")
        self.assertEqual(result[1]["id"], "0002")
        self.assertEqual(result[1]["name"], "Push-up")
        
        # Check that the request was made correctly
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertEqual(args[0], "https://exercisedb.p.rapidapi.com/exercises")
        self.assertEqual(kwargs["headers"]["X-RapidAPI-Key"], settings.EXERCISE_API_KEY)
        self.assertEqual(kwargs["headers"]["X-RapidAPI-Host"], settings.EXERCISE_API_HOST)
    
    @patch('requests.get')
    def test_get_exercise_by_id_from_external_source(self, mock_get):
        # Mock the response from the Exercise API
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "id": "0001",
            "name": "Barbell Bench Press",
            "target": "pectorals",
            "equipment": "barbell",
            "instructions": [
                "Lie on a flat bench with your feet flat on the floor.",
                "Grip the barbell with hands slightly wider than shoulder-width apart.",
                "Lift the barbell off the rack and hold it directly above your chest with arms fully extended.",
                "Lower the barbell to your chest, then press it back up to the starting position."
            ]
        }
        mock_get.return_value = mock_response
        
        # Call the method
        result = self.exercise_service.get_exercise_by_id_from_external_source("0001")
        
        # Check the result
        self.assertEqual(result["id"], "0001")
        self.assertEqual(result["name"], "Barbell Bench Press")
        self.assertEqual(result["target"], "pectorals")
        self.assertEqual(len(result["instructions"]), 4)
        
        # Check that the request was made correctly
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertEqual(args[0], "https://exercisedb.p.rapidapi.com/exercises/exercise/0001")
        self.assertEqual(kwargs["headers"]["X-RapidAPI-Key"], settings.EXERCISE_API_KEY)
        self.assertEqual(kwargs["headers"]["X-RapidAPI-Host"], settings.EXERCISE_API_HOST)
    
    @patch('requests.get')
    def test_get_exercises_by_muscle_from_external_source(self, mock_get):
        # Mock the response from the Exercise API
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {
                "id": "0001",
                "name": "Barbell Bench Press",
                "target": "pectorals",
                "equipment": "barbell"
            },
            {
                "id": "0003",
                "name": "Dumbbell Fly",
                "target": "pectorals",
                "equipment": "dumbbell"
            }
        ]
        mock_get.return_value = mock_response
        
        # Call the method
        result = self.exercise_service.get_exercises_by_muscle_from_external_source("pectorals")
        
        # Check the result
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], "0001")
        self.assertEqual(result[0]["name"], "Barbell Bench Press")
        self.assertEqual(result[1]["id"], "0003")
        self.assertEqual(result[1]["name"], "Dumbbell Fly")
        
        # Check that the request was made correctly
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertEqual(args[0], "https://exercisedb.p.rapidapi.com/exercises/target/pectorals")
        self.assertEqual(kwargs["headers"]["X-RapidAPI-Key"], settings.EXERCISE_API_KEY)
        self.assertEqual(kwargs["headers"]["X-RapidAPI-Host"], settings.EXERCISE_API_HOST)
    
    @patch('app.services.exercise.ExerciseService.get_exercises_by_muscle')
    def test_generate_workout(self, mock_get_exercises_by_muscle):
        # Mock the response from the get_exercises_by_muscle method
        mock_get_exercises_by_muscle.side_effect = [
            [
                {
                    "id": "0001",
                    "name": "Barbell Bench Press",
                    "target": "chest",
                    "equipment": "barbell"
                },
                {
                    "id": "0003",
                    "name": "Dumbbell Fly",
                    "target": "chest",
                    "equipment": "dumbbell"
                }
            ],
            [
                {
                    "id": "0002",
                    "name": "Pull-up",
                    "target": "back",
                    "equipment": "body weight"
                },
                {
                    "id": "0004",
                    "name": "Lat Pulldown",
                    "target": "back",
                    "equipment": "cable"
                }
            ]
        ]
        
        # Call the method
        result = self.exercise_service.generate_workout(
            muscle_groups=["chest", "back"],
            available_equipment=["barbell", "dumbbell", "body weight", "cable"],
            fitness_level="intermediate",
            workout_duration_minutes=60
        )
        
        # Check the result
        self.assertEqual(len(result), 4)  # 2 exercises per muscle group
        
        # Check that the exercises have the expected properties
        for exercise in result:
            self.assertIn("exercise_id", exercise)
            self.assertIn("name", exercise)
            self.assertIn("muscle_group", exercise)
            self.assertIn("equipment", exercise)
            self.assertIn("sets", exercise)
            self.assertIn("reps", exercise)
            self.assertIn("rest_seconds", exercise)
            self.assertIn("order", exercise)
        
        # Check that the exercises are ordered correctly
        self.assertEqual(result[0]["order"], 1)
        self.assertEqual(result[1]["order"], 2)
        self.assertEqual(result[2]["order"], 3)
        self.assertEqual(result[3]["order"], 4)
        
        # Check that the fitness level affects the workout parameters
        self.assertEqual(result[0]["sets"], 4)  # intermediate level
        self.assertEqual(result[0]["reps"], "10-12")  # intermediate level
        self.assertEqual(result[0]["rest_seconds"], 45)  # intermediate level

if __name__ == '__main__':
    unittest.main()
