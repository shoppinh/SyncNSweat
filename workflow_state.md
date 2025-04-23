# Workflow State & Rules (STM + Rules + Log)

*This file contains the dynamic state, embedded rules, active plan, and log for the current session.*
*It is read and updated frequently by the AI during its operational loop.*

---

## State

*Holds the current status of the workflow.*

```yaml
Phase: CONSTRUCT # Current workflow phase (ANALYZE, BLUEPRINT, CONSTRUCT, VALIDATE, BLUEPRINT_REVISE)
Status: IN_PROGRESS # Current status (READY, IN_PROGRESS, BLOCKED_*, NEEDS_*, COMPLETED)
CurrentTaskID: PHASE_0_SETUP # Identifier for the main task being worked on
CurrentStep: STEP_7 # Identifier for the specific step in the plan being executed
```

---

## Plan

*Contains the step-by-step implementation plan generated during the BLUEPRINT phase.*

*Task: Phase 0 - Foundation & Setup*

### Environment Setup
1. Install Node.js and npm/yarn for React Native development
   - Download and install Node.js LTS version (v20.x or later) from nodejs.org
   - Verify installation with `node -v` and `npm -v`
   - Install Yarn globally with `npm install -g yarn` (optional but recommended)
   - Verify Yarn installation with `yarn -v`

2. Install Python and pip/conda for FastAPI backend
   - Verify installation with `python --version`
   - If not installed, Download and install Python 3.11+ from python.org
   - Ensure pip is installed and updated with `python -m pip install --upgrade pip`
   - Create a virtual environment with `python -m venv venv`
   - Activate virtual environment (Windows: `venv\Scripts\activate`, Unix: `source venv/bin/activate`)

3. Install PostgreSQL for database
   - Download and install PostgreSQL 13+ from postgresql.org
   - Set a secure password for the postgres user during installation
   - Verify installation with `psql --version`
   - Create a new database for the project with `createdb syncnsweat`

4. Set up VS Code with relevant extensions for React Native and Python development
   - Install VS Code from code.visualstudio.com
   - Install Python extension for VS Code
   - Install ESLint and Prettier extensions for JavaScript/TypeScript
   - Install React Native Tools extension
   - Install SQLTools extension for PostgreSQL integration
   - Configure workspace settings for consistent formatting

### Project Initialization
1. Create React Native project using Expo with TypeScript
   - Navigate to desired directory: `cd c:\Dev\kien.mac\syncnsweat`
   - Create Expo project with TypeScript: `npx create-expo-app SyncSweatApp --template expo-template-blank-typescript`
   - Verify project creation by navigating to the directory: `cd SyncSweatApp`
   - Install Expo SDK: `npx expo install expo-dev-client`
   - Test the app with: `npx expo start`

2. Set up Python backend project structure with FastAPI
   - Create a backend directory: `mkdir backend && cd backend`
   - Activate virtual environment if not already active
   - Install FastAPI and dependencies: `pip install fastapi uvicorn sqlalchemy alembic psycopg2-binary python-dotenv`
   - Create basic directory structure:
     ```
     backend/
     ├── app/
     │   ├── __init__.py
     │   ├── main.py
     │   ├── api/
     │   │   ├── __init__.py
     │   │   └── endpoints/
     │   ├── core/
     │   │   ├── __init__.py
     │   │   └── config.py
     │   ├── db/
     │   │   ├── __init__.py
     │   │   └── session.py
     │   └── models/
     │       └── __init__.py
     ├── requirements.txt
     └── .env
     ```
   - Create a basic FastAPI app in `app/main.py`
   - Create a requirements.txt file with all dependencies

3. Initialize Git repository
   - Navigate to project root: `cd c:\Dev\kien.mac\syncnsweat`
   - Initialize Git repository: `git init`
   - Create .gitignore file with appropriate entries for React Native and Python
   - Make initial commit: `git add . && git commit -m "Initial project setup"`

4. Create initial README.md with project overview
   - Create README.md file with project name, description, and setup instructions
   - Include sections for frontend and backend setup
   - Add information about required environment variables
   - Include basic usage instructions

### Database Setup
1. Create initial PostgreSQL database
   - Connect to PostgreSQL: `psql -U postgres`
   - Create database: `CREATE DATABASE syncnsweat;`
   - Create a dedicated user: `CREATE USER syncnsweat_user WITH PASSWORD 'secure_password';`
   - Grant privileges: `GRANT ALL PRIVILEGES ON DATABASE syncnsweat TO syncnsweat_user;`
   - Verify connection with new user: `psql -U syncnsweat_user -d syncnsweat`

2. Choose and set up ORM (SQLAlchemy)
   - Ensure SQLAlchemy is installed: `pip install sqlalchemy`
   - Create database connection module in `app/db/session.py`:
     ```python
     from sqlalchemy import create_engine
     from sqlalchemy.ext.declarative import declarative_base
     from sqlalchemy.orm import sessionmaker
     from app.core.config import settings

     engine = create_engine(settings.DATABASE_URI)
     SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
     Base = declarative_base()

     def get_db():
         db = SessionLocal()
         try:
             yield db
         finally:
             db.close()
     ```
   - Create configuration module in `app/core/config.py` for database URI

3. Set up migration tool (Alembic)
   - Install Alembic: `pip install alembic`
   - Initialize Alembic: `alembic init migrations`
   - Configure Alembic to use SQLAlchemy models
   - Update `alembic.ini` with database connection string
   - Create initial migration script: `alembic revision --autogenerate -m "Initial tables"`

4. Design initial core schema (Users, Profiles, Basic Preferences)
   - Create User model in `app/models/user.py`:
     ```python
     from sqlalchemy import Boolean, Column, Integer, String, DateTime
     from sqlalchemy.sql import func
     from app.db.session import Base

     class User(Base):
         __tablename__ = "users"

         id = Column(Integer, primary_key=True, index=True)
         email = Column(String, unique=True, index=True)
         hashed_password = Column(String)
         is_active = Column(Boolean, default=True)
         created_at = Column(DateTime(timezone=True), server_default=func.now())
         updated_at = Column(DateTime(timezone=True), onupdate=func.now())
     ```
   - Create Profile model in `app/models/profile.py`
   - Create Preferences model in `app/models/preferences.py`
   - Define relationships between models
   - Run migration: `alembic upgrade head`

### API Setup
1. Set up basic FastAPI app structure
   - Create main FastAPI application in `app/main.py`:
     ```python
     from fastapi import FastAPI
     from app.api.endpoints import router as api_router
     from app.core.config import settings

     app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

     app.include_router(api_router, prefix=settings.API_V1_STR)

     @app.get("/")
     def root():
         return {"message": "Welcome to Sync & Sweat API"}

     if __name__ == "__main__":
         import uvicorn
         uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
     ```
   - Create configuration in `app/core/config.py`:
     ```python
     from pydantic import BaseSettings
     from typing import Optional
     import os
     from dotenv import load_dotenv

     load_dotenv()

     class Settings(BaseSettings):
         PROJECT_NAME: str = "Sync & Sweat"
         VERSION: str = "0.1.0"
         API_V1_STR: str = "/api/v1"
         SECRET_KEY: str = os.getenv("SECRET_KEY", "development_secret_key")
         DATABASE_URI: str = os.getenv("DATABASE_URI", "postgresql://syncnsweat_user:secure_password@localhost/syncnsweat")
         ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

     settings = Settings()
     ```

2. Implement REST API design principles
   - Create API router in `app/api/endpoints/__init__.py`:
     ```python
     from fastapi import APIRouter
     from app.api.endpoints import users, auth, profiles, workouts, playlists

     router = APIRouter()

     router.include_router(auth.router, prefix="/auth", tags=["auth"])
     router.include_router(users.router, prefix="/users", tags=["users"])
     router.include_router(profiles.router, prefix="/profiles", tags=["profiles"])
     router.include_router(workouts.router, prefix="/workouts", tags=["workouts"])
     router.include_router(playlists.router, prefix="/playlists", tags=["playlists"])
     ```
   - Create placeholder endpoint modules (e.g., `users.py`, `auth.py`, etc.)
   - Implement consistent response models and error handling

3. Set up basic API routing
   - Create a basic users endpoint in `app/api/endpoints/users.py`:
     ```python
     from fastapi import APIRouter, Depends, HTTPException
     from sqlalchemy.orm import Session
     from app.db.session import get_db

     router = APIRouter()

     @router.get("/")
     def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
         return {"message": "List of users will be returned here"}

     @router.get("/{user_id}")
     def get_user(user_id: int, db: Session = Depends(get_db)):
         return {"message": f"User with ID {user_id} will be returned here"}
     ```
   - Create similar placeholder endpoints for other resources

4. Create initial API documentation
   - FastAPI automatically generates OpenAPI documentation
   - Add detailed docstrings to all endpoints
   - Create a `docs/api.md` file with API overview and usage examples
   - Document authentication flow and required headers
   - Include example requests and responses

### External Services Integration
1. Register app on Spotify Developer Dashboard
   - Visit [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
   - Create a new account if needed
   - Click "Create an App" and fill in the required information:
     - App name: "Sync & Sweat"
     - App description: "A fitness app that generates personalized workout schedules and music playlists"
     - Website: Can be left blank for development
     - Redirect URI: Set to `http://localhost:8000/api/v1/auth/spotify/callback` for local development
   - Accept the terms and conditions

2. Obtain Spotify Client ID & Client Secret
   - After creating the app, note down the Client ID displayed on the dashboard
   - Click "Show Client Secret" to reveal and note down the Client Secret
   - Store these securely in the `.env` file:
     ```
     SPOTIFY_CLIENT_ID=your_client_id_here
     SPOTIFY_CLIENT_SECRET=your_client_secret_here
     ```

3. Test basic OAuth connection locally
   - Create a Spotify service module in `app/services/spotify.py`:
     ```python
     import base64
     import requests
     from app.core.config import settings

     class SpotifyService:
         def __init__(self):
             self.client_id = settings.SPOTIFY_CLIENT_ID
             self.client_secret = settings.SPOTIFY_CLIENT_SECRET
             self.auth_url = "https://accounts.spotify.com/authorize"
             self.token_url = "https://accounts.spotify.com/api/token"
             self.api_base_url = "https://api.spotify.com/v1"

         def get_auth_url(self, redirect_uri, state=None):
             params = {
                 "client_id": self.client_id,
                 "response_type": "code",
                 "redirect_uri": redirect_uri,
                 "scope": "user-read-private user-read-email playlist-read-private playlist-read-collaborative"
             }
             if state:
                 params["state"] = state

             auth_url = f"{self.auth_url}?" + "&".join([f"{k}={v}" for k, v in params.items()])
             return auth_url

         def get_access_token(self, code, redirect_uri):
             auth_header = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
             headers = {
                 "Authorization": f"Basic {auth_header}",
                 "Content-Type": "application/x-www-form-urlencoded"
             }
             data = {
                 "grant_type": "authorization_code",
                 "code": code,
                 "redirect_uri": redirect_uri
             }

             response = requests.post(self.token_url, headers=headers, data=data)
             return response.json()
     ```
   - Create a simple test endpoint in `app/api/endpoints/auth.py` to test the OAuth flow

3. Obtain API keys for chosen Exercise API
   - Sign up for the selected Exercise API service
   - Generate API keys as required by the service
   - Store the API key securely in the `.env` file:
     ```
     EXERCISE_API_KEY=your_api_key_here
     EXERCISE_API_HOST=api_host_if_required
     ```

4. Test basic API calls to understand data structure
   - Create an Exercise service module in `app/services/exercise.py`:
     ```python
     import requests
     from app.core.config import settings

     class ExerciseService:
         def __init__(self):
             self.api_key = settings.EXERCISE_API_KEY
             self.api_host = settings.EXERCISE_API_HOST
             self.api_url = "https://exercisedb.p.rapidapi.com"  # Example for ExerciseDB

         def get_exercises(self, params=None):
             headers = {
                 "X-RapidAPI-Key": self.api_key,
                 "X-RapidAPI-Host": self.api_host
             }

             response = requests.get(f"{self.api_url}/exercises", headers=headers, params=params)
             return response.json()

         def get_exercise_by_id(self, exercise_id):
             headers = {
                 "X-RapidAPI-Key": self.api_key,
                 "X-RapidAPI-Host": self.api_host
             }

             response = requests.get(f"{self.api_url}/exercises/exercise/{exercise_id}", headers=headers)
             return response.json()

         def get_exercises_by_muscle(self, muscle):
             headers = {
                 "X-RapidAPI-Key": self.api_key,
                 "X-RapidAPI-Host": self.api_host
             }

             response = requests.get(f"{self.api_url}/exercises/target/{muscle}", headers=headers)
             return response.json()
     ```
   - Create a simple test script to verify API functionality
   - Document the data structure and available endpoints

### Basic CI/CD
1. Set up GitHub Actions for linting/testing on pushes
   - Create a `.github/workflows` directory in the project root
   - Create a workflow file for the frontend in `.github/workflows/frontend.yml`:
     ```yaml
     name: Frontend CI

     on:
       push:
         branches: [ main ]
         paths:
           - 'SyncSweatApp/**'
       pull_request:
         branches: [ main ]
         paths:
           - 'SyncSweatApp/**'

     jobs:
       build:
         runs-on: ubuntu-latest

         steps:
         - uses: actions/checkout@v2
         - name: Use Node.js
           uses: actions/setup-node@v2
           with:
             node-version: '16.x'
             cache: 'npm'
             cache-dependency-path: SyncSweatApp/package-lock.json

         - name: Install dependencies
           run: cd SyncSweatApp && npm install

         - name: Install Expo CLI
           run: npm install -g expo-cli

         - name: Lint
           run: cd SyncSweatApp && npm run lint

         - name: TypeScript check
           run: cd SyncSweatApp && npx tsc --noEmit

         - name: Run tests
           run: cd SyncSweatApp && npm test
     ```
   - Create a workflow file for the backend in `.github/workflows/backend.yml`:
     ```yaml
     name: Backend CI

     on:
       push:
         branches: [ main ]
         paths:
           - 'backend/**'
       pull_request:
         branches: [ main ]
         paths:
           - 'backend/**'

     jobs:
       build:
         runs-on: ubuntu-latest

         services:
           postgres:
             image: postgres:13
             env:
               POSTGRES_USER: postgres
               POSTGRES_PASSWORD: postgres
               POSTGRES_DB: test_db
             ports:
               - 5432:5432
             options: --health-cmd pg_isready --health-interval 10s --health-timeout 5s --health-retries 5

         steps:
         - uses: actions/checkout@v2
         - name: Set up Python
           uses: actions/setup-python@v2
           with:
             python-version: '3.9'
             cache: 'pip'
             cache-dependency-path: backend/requirements.txt

         - name: Install dependencies
           run: |
             cd backend
             python -m pip install --upgrade pip
             pip install -r requirements.txt
             pip install pytest pytest-cov flake8

         - name: Lint with flake8
           run: |
             cd backend
             flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

         - name: Test with pytest
           run: |
             cd backend
             pytest --cov=app
           env:
             DATABASE_URI: postgresql://postgres:postgres@localhost:5432/test_db
             SECRET_KEY: test_secret_key
     ```

2. Configure basic testing framework for both frontend and backend
   - Set up Jest for Expo frontend testing:
     - Install Jest and related dependencies: `cd SyncSweatApp && npx expo install jest-expo jest @testing-library/react-native @testing-library/jest-native`
     - Create a basic Jest configuration in `SyncSweatApp/jest.config.js` using the Expo preset
     - Add test script to `package.json`: `"test": "jest --watchAll"`
     - Create a sample test file in `SyncSweatApp/__tests__/App-test.tsx`
   - Set up pytest for Python backend testing:
     - Install pytest and related dependencies: `cd backend && pip install pytest pytest-cov`
     - Create a `backend/tests` directory with `__init__.py`
     - Create a `backend/tests/conftest.py` file with test fixtures
     - Create sample test files for API endpoints and services
     - Add a `.coveragerc` file to configure coverage reporting

### Technology Decisions
1. Select navigation library (React Navigation with Expo)
   - Install React Navigation: `cd SyncSweatApp && npx expo install @react-navigation/native`
   - Install dependencies: `npx expo install react-native-screens react-native-safe-area-context`
   - Install navigation stack: `npx expo install @react-navigation/native-stack @react-navigation/bottom-tabs`
   - Create a basic navigation structure in `SyncSweatApp/src/navigation/index.tsx`:
     ```tsx
     import React from 'react';
     import { NavigationContainer } from '@react-navigation/native';
     import { createNativeStackNavigator } from '@react-navigation/native-stack';
     import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';

     // Import screens
     import LoginScreen from '../screens/LoginScreen';
     import SignupScreen from '../screens/SignupScreen';
     import HomeScreen from '../screens/HomeScreen';
     import ProfileScreen from '../screens/ProfileScreen';
     import WorkoutScreen from '../screens/WorkoutScreen';

     const Stack = createNativeStackNavigator();
     const Tab = createBottomTabNavigator();

     const MainTabs = () => {
       return (
         <Tab.Navigator>
           <Tab.Screen name="Home" component={HomeScreen} />
           <Tab.Screen name="Workout" component={WorkoutScreen} />
           <Tab.Screen name="Profile" component={ProfileScreen} />
         </Tab.Navigator>
       );
     };

     const AppNavigator = () => {
       return (
         <NavigationContainer>
           <Stack.Navigator initialRouteName="Login">
             <Stack.Screen name="Login" component={LoginScreen} options={{ headerShown: false }} />
             <Stack.Screen name="Signup" component={SignupScreen} options={{ headerShown: false }} />
             <Stack.Screen name="Main" component={MainTabs} options={{ headerShown: false }} />
           </Stack.Navigator>
         </NavigationContainer>
       );
     };

     export default AppNavigator;
     ```

2. Choose state management approach (Context API, Redux Toolkit, or Zustand)
   - Evaluate options:
     - Context API: Built into React, simpler for smaller apps
     - Redux Toolkit: More structured, better for complex state
     - Zustand: Lightweight alternative to Redux
   - Decision: Use Context API for initial development with potential to migrate to Redux Toolkit if needed
   - Implement a basic auth context in `SyncSweatApp/src/contexts/AuthContext.tsx`:
     ```tsx
     import React, { createContext, useState, useContext, ReactNode } from 'react';

     type AuthContextType = {
       isAuthenticated: boolean;
       user: any | null;
       login: (email: string, password: string) => Promise<void>;
       logout: () => void;
       signup: (email: string, password: string, name: string) => Promise<void>;
     };

     const AuthContext = createContext<AuthContextType | undefined>(undefined);

     export const AuthProvider = ({ children }: { children: ReactNode }) => {
       const [isAuthenticated, setIsAuthenticated] = useState(false);
       const [user, setUser] = useState<any | null>(null);

       const login = async (email: string, password: string) => {
         // TODO: Implement actual API call
         setIsAuthenticated(true);
         setUser({ email });
       };

       const logout = () => {
         setIsAuthenticated(false);
         setUser(null);
       };

       const signup = async (email: string, password: string, name: string) => {
         // TODO: Implement actual API call
         setIsAuthenticated(true);
         setUser({ email, name });
       };

       return (
         <AuthContext.Provider value={{ isAuthenticated, user, login, logout, signup }}>
           {children}
         </AuthContext.Provider>
       );
     };

     export const useAuth = () => {
       const context = useContext(AuthContext);
       if (context === undefined) {
         throw new Error('useAuth must be used within an AuthProvider');
       }
       return context;
     };
     ```

3. Select styling approach (Styled Components or NativeWind)
   - Evaluate options:
     - Styled Components: Component-based styling with CSS-in-JS
     - NativeWind: Tailwind CSS for React Native
   - Decision: Use Styled Components for more flexibility
   - Install Styled Components: `cd SyncSweatApp && yarn add styled-components @types/styled-components @types/styled-components-react-native`
   - Create a theme file in `SyncSweatApp/src/theme/index.ts`:
     ```typescript
     export const theme = {
       colors: {
         primary: '#4361EE',
         secondary: '#3A0CA3',
         background: '#F8F9FA',
         text: '#212529',
         lightText: '#6C757D',
         error: '#E63946',
         success: '#2A9D8F',
         warning: '#F4A261',
         white: '#FFFFFF',
         black: '#000000',
       },
       spacing: {
         xs: 4,
         sm: 8,
         md: 16,
         lg: 24,
         xl: 32,
         xxl: 48,
       },
       fontSizes: {
         xs: 12,
         sm: 14,
         md: 16,
         lg: 18,
         xl: 20,
         xxl: 24,
       },
       borderRadius: {
         sm: 4,
         md: 8,
         lg: 16,
         full: 9999,
       },
     };

     export type Theme = typeof theme;
     ```

4. Finalize backend framework details and middleware
   - Confirm FastAPI as the backend framework
   - Select and install middleware components:
     - CORS: `pip install fastapi-cors`
     - Authentication: JWT with `pip install python-jose[cryptography] passlib[bcrypt]`
     - Request validation: Built into FastAPI with Pydantic
     - Database: SQLAlchemy ORM with PostgreSQL
   - Update the main FastAPI app in `app/main.py` to include middleware:
     ```python
     from fastapi import FastAPI
     from fastapi.middleware.cors import CORSMiddleware
     from app.api.endpoints import router as api_router
     from app.core.config import settings

     app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

     # Set up CORS
     origins = [
         "http://localhost",
         "http://localhost:3000",
         "http://localhost:8000",
         "http://localhost:19006",  # React Native Expo web
     ]

     app.add_middleware(
         CORSMiddleware,
         allow_origins=origins,
         allow_credentials=True,
         allow_methods=["*"],
         allow_headers=["*"],
     )

     app.include_router(api_router, prefix=settings.API_V1_STR)

     @app.get("/")
     def root():
         return {"message": "Welcome to Sync & Sweat API"}
     ```


---

## Rules

*Embedded rules governing the AI's autonomous operation.*

**# --- Core Workflow Rules ---**

RULE_WF_PHASE_ANALYZE:
  **Constraint:** Goal is understanding request/context. NO solutioning or implementation planning.

RULE_WF_PHASE_BLUEPRINT:
  **Constraint:** Goal is creating a detailed, unambiguous step-by-step plan. NO code implementation.

RULE_WF_PHASE_CONSTRUCT:
  **Constraint:** Goal is executing the `## Plan` exactly. NO deviation. If issues arise, trigger error handling or revert phase.

RULE_WF_PHASE_VALIDATE:
  **Constraint:** Goal is verifying implementation against `## Plan` and requirements using tools. NO new implementation.

RULE_WF_TRANSITION_01:
  **Trigger:** Explicit user command (`@analyze`, `@blueprint`, `@construct`, `@validate`).
  **Action:** Update `State.Phase` accordingly. Log phase change.

RULE_WF_TRANSITION_02:
  **Trigger:** AI determines current phase constraint prevents fulfilling user request OR error handling dictates phase change (e.g., RULE_ERR_HANDLE_TEST_01).
  **Action:** Log the reason. Update `State.Phase` (e.g., to `BLUEPRINT_REVISE`). Set `State.Status` appropriately (e.g., `NEEDS_PLAN_APPROVAL`). Report to user.

**# --- Initialization & Resumption Rules ---**

RULE_INIT_01:
  **Trigger:** AI session/task starts AND `workflow_state.md` is missing or empty.
  **Action:**
    1. Create `workflow_state.md` with default structure.
    2. Read `project_config.md` (prompt user if missing).
    3. Set `State.Phase = ANALYZE`, `State.Status = READY`.
    4. Log "Initialized new session."
    5. Prompt user for the first task.

RULE_INIT_02:
  **Trigger:** AI session/task starts AND `workflow_state.md` exists.
  **Action:**
    1. Read `project_config.md`.
    2. Read existing `workflow_state.md`.
    3. Log "Resumed session."
    4. Check `State.Status`: Handle READY, COMPLETED, BLOCKED_*, NEEDS_*, IN_PROGRESS appropriately (prompt user or report status).

RULE_INIT_03:
  **Trigger:** User confirms continuation via RULE_INIT_02 (for IN_PROGRESS state).
  **Action:** Proceed with the next action based on loaded state and rules.

**# --- Memory Management Rules ---**

RULE_MEM_READ_LTM_01:
  **Trigger:** Start of a new major task or phase.
  **Action:** Read `project_config.md`. Log action.

RULE_MEM_READ_STM_01:
  **Trigger:** Before *every* decision/action cycle.
  **Action:** Read `workflow_state.md`.

RULE_MEM_UPDATE_STM_01:
  **Trigger:** After *every* significant action or information receipt.
  **Action:** Immediately update relevant sections (`## State`, `## Plan`, `## Log`) in `workflow_state.md` and save.

RULE_MEM_UPDATE_LTM_01:
  **Trigger:** User command (`@config/update`) OR end of successful VALIDATE phase for significant change.
  **Action:** Propose concise updates to `project_config.md` based on `## Log`/diffs. Set `State.Status = NEEDS_LTM_APPROVAL`. Await user confirmation.

RULE_MEM_VALIDATE_01:
  **Trigger:** After updating `workflow_state.md` or `project_config.md`.
  **Action:** Perform internal consistency check. If issues found, log and set `State.Status = NEEDS_CLARIFICATION`.

**# --- Tool Integration Rules (Cursor Environment) ---**

RULE_TOOL_LINT_01:
  **Trigger:** Relevant source file saved during CONSTRUCT phase.
  **Action:** Instruct Cursor terminal to run lint command. Log attempt. On completion, parse output, log result, set `State.Status = BLOCKED_LINT` if errors.

RULE_TOOL_FORMAT_01:
  **Trigger:** Relevant source file saved during CONSTRUCT phase.
  **Action:** Instruct Cursor to apply formatter or run format command via terminal. Log attempt.

RULE_TOOL_TEST_RUN_01:
  **Trigger:** Command `@validate` or entering VALIDATE phase.
  **Action:** Instruct Cursor terminal to run test suite. Log attempt. On completion, parse output, log result, set `State.Status = BLOCKED_TEST` if failures, `TESTS_PASSED` if success.

RULE_TOOL_APPLY_CODE_01:
  **Trigger:** AI determines code change needed per `## Plan` during CONSTRUCT phase.
  **Action:** Generate modification. Instruct Cursor to apply it. Log action.

**# --- Error Handling & Recovery Rules ---**

RULE_ERR_HANDLE_LINT_01:
  **Trigger:** `State.Status` is `BLOCKED_LINT`.
  **Action:** Analyze error in `## Log`. Attempt auto-fix if simple/confident. Apply fix via RULE_TOOL_APPLY_CODE_01. Re-run lint via RULE_TOOL_LINT_01. If success, reset `State.Status`. If fail/complex, set `State.Status = BLOCKED_LINT_UNRESOLVED`, report to user.

RULE_ERR_HANDLE_TEST_01:
  **Trigger:** `State.Status` is `BLOCKED_TEST`.
  **Action:** Analyze failure in `## Log`. Attempt auto-fix if simple/localized/confident. Apply fix via RULE_TOOL_APPLY_CODE_01. Re-run failed test(s) or suite via RULE_TOOL_TEST_RUN_01. If success, reset `State.Status`. If fail/complex, set `State.Phase = BLUEPRINT_REVISE`, `State.Status = NEEDS_PLAN_APPROVAL`, propose revised `## Plan` based on failure analysis, report to user.

RULE_ERR_HANDLE_GENERAL_01:
  **Trigger:** Unexpected error or ambiguity.
  **Action:** Log error/situation to `## Log`. Set `State.Status = BLOCKED_UNKNOWN`. Report to user, request instructions.

---

## Log

*A chronological log of significant actions, events, tool outputs, and decisions.*
*(This section will be populated by the AI during operation)*

*Example:*
*   `[2025-03-26 17:55:00] Initialized new session.`
*   `[2025-03-26 17:55:15] User task: Implement login feature.`
*   `[2025-03-26 17:55:20] State.Phase changed to ANALYZE.`
*   `[2025-03-26 17:56:00] Read project_config.md.`
*   ...

*Actual Log:*

[2023-11-15 10:00:00] Initialized new session.
[2023-11-15 10:00:15] User task: Begin Phase 0 - Foundation & Setup.
[2023-11-15 10:00:20] State.Phase changed to ANALYZE.
[2023-11-15 10:00:30] Read project_overview.md.
[2023-11-15 10:01:00] Updated workflow_state.md with Phase 0 plan.
[2023-11-15 10:05:00] Completed analysis of Phase 0 requirements.
[2023-11-15 10:05:15] State.Phase changed to BLUEPRINT.
[2023-11-15 10:05:30] Created detailed implementation plan for Phase 0.
[2023-11-15 10:30:00] Completed detailed blueprint for all sections of Phase 0.
[2023-11-15 10:30:15] State.Phase changed to CONSTRUCT.
[2023-11-15 10:30:30] Ready to begin implementation of Phase 0 tasks.
[2023-11-15 10:45:00] User requested to use Expo framework instead of bare React Native.
[2023-11-15 10:45:15] Updated project initialization section to use Expo.
[2023-11-15 10:46:00] Updated React Navigation setup for Expo compatibility.
[2023-11-15 10:46:30] Updated testing configuration for Expo.
[2023-11-15 10:47:00] Updated GitHub Actions workflow for Expo.
[2023-11-15 11:00:00] Started implementation of Environment Setup (STEP_1).
[2023-11-15 11:00:15] Verified Node.js (v22.11.0) and npm (11.2.0) are installed.
[2023-11-15 11:00:30] Verified Python (3.12.6) is installed.
[2023-11-15 11:00:45] PostgreSQL is not installed or not in PATH.
[2023-11-15 11:10:00] Created project directory structure.
[2023-11-15 11:15:00] Installed Expo CLI and created Expo project with TypeScript template.
[2023-11-15 11:20:00] Created Python virtual environment and installed FastAPI dependencies.
[2023-11-15 11:25:00] Set up basic FastAPI application structure.
[2023-11-15 11:30:00] Created configuration files for backend.
[2023-11-15 11:35:00] Created project README.md and .gitignore files.
[2023-11-15 11:40:00] Initialized Git repository and made initial commit.
[2023-11-15 11:45:00] Completed Project Initialization (STEP_2).
[2023-11-15 11:45:15] Moving to Database Setup (STEP_3).
[2023-11-15 11:50:00] Created database models for User, Profile, Preferences, and Workout.
[2023-11-15 11:55:00] Set up Alembic for database migrations.
[2023-11-15 12:00:00] Configured Alembic to use SQLAlchemy models.
[2023-11-15 12:05:00] Generated initial migration script for database tables.
[2023-11-15 12:10:00] Completed Database Setup (STEP_3).
[2023-11-15 12:10:15] Moving to API Setup (STEP_4).
[2023-11-15 12:15:00] Created API schemas for User, Profile, Preferences, and Workout.
[2023-11-15 12:20:00] Implemented authentication endpoints and security utilities.
[2023-11-15 12:25:00] Implemented user and profile endpoints.
[2023-11-15 12:30:00] Implemented workout and exercise endpoints.
[2023-11-15 12:35:00] Implemented Spotify integration endpoints.
[2023-11-15 12:40:00] Created service classes for Spotify and Exercise APIs.
[2023-11-15 12:45:00] Completed API Setup (STEP_4).
[2023-11-15 12:45:15] Moving to External Services Integration (STEP_5).
[2023-11-15 12:50:00] Created unit tests for Spotify service.
[2023-11-15 12:55:00] Created unit tests for Exercise service.
[2023-11-15 13:00:00] Installed required dependencies for external services.
[2023-11-15 13:05:00] Verified external services integration with tests.
[2023-11-15 13:10:00] Completed External Services Integration (STEP_5).
[2023-11-15 13:10:15] Moving to Basic CI/CD (STEP_6).
[2023-11-15 13:15:00] Created GitHub Actions workflow for frontend.
[2023-11-15 13:20:00] Created GitHub Actions workflow for backend.
[2023-11-15 13:25:00] Set up Jest testing for frontend.
[2023-11-15 13:30:00] Created ESLint configuration for frontend.
[2023-11-15 13:35:00] Completed Basic CI/CD (STEP_6).
[2023-11-15 13:35:15] Moving to Technology Decisions (STEP_7).