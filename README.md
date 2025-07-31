# Quiz Master V2 - Prototype

A simple multi-user quiz application with admin and user roles, built with Flask backend and Vue3 frontend.

## Features

### Admin Features
- **Default Admin Login**: admin@quizmaster.com / admin123
- Create and manage subjects
- Create chapters under subjects  
- Create quizzes under chapters
- Add multiple-choice questions to quizzes
- View quiz management dashboard

### User Features
- User registration and login
- Browse available quizzes by subject/chapter
- Take timed quizzes with multiple-choice questions
- View quiz results and scoring
- Track quiz history and previous scores

### Technical Features
- **Backend**: Flask with SQLite database
- **Frontend**: Vue3 with Bootstrap styling
- **Authentication**: Session-based with role management
- **Timer**: Real-time countdown during quiz attempts
- **Responsive**: Works on mobile and desktop

## Quick Start

### Prerequisites
- Python 3.7+
- Modern web browser

### Installation & Setup

1. **Install Python dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Start the Flask backend:**
   ```bash
   python app.py
   ```
   
   The backend will start on http://localhost:5000

3. **Open the frontend:**
   - Open `frontend/index.html` in your web browser, or
   - Use a local server like `python -m http.server 8080` in the frontend directory

### Usage

1. **Admin Access:**
   - Login with: admin@quizmaster.com / admin123
   - Create subjects, chapters, quizzes, and questions
   - Manage the quiz system

2. **User Access:**
   - Register a new user account
   - Browse and take available quizzes
   - View scores and quiz history

## Project Structure

```
quiz-master-v2/
├── backend/
│   ├── app.py              # Flask application with all API endpoints
│   ├── requirements.txt    # Python dependencies
│   └── quiz_master.db     # SQLite database (auto-created)
├── frontend/
│   └── index.html         # Vue3 SPA with Bootstrap styling
├── README.md
└── prompt.md              # Original requirements
```

## Database Schema

- **users**: User accounts with role management
- **subjects**: Quiz subjects/categories
- **chapters**: Subdivisions within subjects
- **quizzes**: Quiz instances with timing
- **questions**: Multiple-choice questions
- **scores**: User quiz attempt results

## API Endpoints

### Authentication
- `POST /api/login` - User login
- `POST /api/register` - User registration  
- `POST /api/logout` - User logout

### Content Management (Admin)
- `GET/POST /api/subjects` - Manage subjects
- `GET /api/subjects/{id}/chapters` - Get chapters
- `POST /api/chapters` - Create chapters
- `GET /api/chapters/{id}/quizzes` - Get quizzes
- `POST /api/quizzes` - Create quizzes
- `POST /api/questions` - Add questions

### Quiz Taking (Users)
- `GET /api/quiz/{id}` - Get quiz with questions
- `POST /api/quiz/{id}/submit` - Submit quiz answers
- `GET /api/user/scores` - Get user's quiz history

## Notes

- This is a functional prototype built for demonstration
- Database is automatically initialized with an admin user
- All operations work in-memory with SQLite
- Frontend uses CDN resources for quick setup
- Session-based authentication with CORS support