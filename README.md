# Sync & Sweat

A personalized fitness companion that eliminates workout and music monotony by generating dynamic weekly gym schedules and curating fresh Spotify playlists.

## Features

- User profiling & goal setting
- AI-powered weekly schedule generation
- Daily exercise rotation engine
- Spotify playlist integration & rotation
- Personalized workout recommendations
- Clean, intuitive mobile interface

## Tech Stack

- **Frontend**: React Native with Expo (TypeScript)
- **Backend**: Python with FastAPI
- **Database**: PostgreSQL
- **APIs**: Spotify Web API, ExerciseDB API

## Getting Started

### Prerequisites

- Node.js (v16+)
- npm or yarn
- Python 3.9+
- PostgreSQL
- Spotify Developer Account
- ExerciseDB API Key

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd SyncSweatApp
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the Expo development server:
   ```
   npx expo start
   ```

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Activate the virtual environment:
   ```
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a `.env` file based on the provided example
   - Add your Spotify API credentials and ExerciseDB API key

5. Run the development server:
   ```
   uvicorn app.main:app --reload
   ```

## Project Structure

```
syncnsweat/
├── SyncSweatApp/         # React Native frontend
│   ├── src/
│   │   ├── components/   # Reusable UI components
│   │   ├── screens/      # App screens
│   │   ├── navigation/   # Navigation configuration
│   │   ├── contexts/     # React contexts
│   │   ├── services/     # API services
│   │   ├── hooks/        # Custom hooks
│   │   ├── utils/        # Utility functions
│   │   └── theme/        # Styling and theme
│   └── ...
│
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Core configuration
│   │   ├── db/           # Database setup
│   │   ├── models/       # Database models
│   │   └── services/     # Business logic
│   └── ...
│
└── ...
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Spotify Web API
- ExerciseDB API
