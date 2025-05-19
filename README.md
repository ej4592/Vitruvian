# Exercise Competition App

A full-stack web application that allows users to create groups and compete in exercises with friends. The app tracks scores and rankings across multiple events.

## Features

- User authentication and profile management
- Group creation and management
- Exercise event creation and tracking
- Score calculation and ranking system
- Real-time updates and leaderboards

## Tech Stack

- Frontend: Streamlit
- Backend: FastAPI
- Database: SQLite
- Authentication: JWT

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the backend server:
```bash
uvicorn app.backend.main:app --reload
```

4. Run the frontend:
```bash
streamlit run app/frontend/app.py
```

## Project Structure

```
app/
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── database.py
├── frontend/
│   ├── app.py
│   └── pages/
└── database/
    └── exercise_competition.db
```
