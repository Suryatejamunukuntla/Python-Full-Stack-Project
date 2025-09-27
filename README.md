## Project Title: Collaborative Online Notes App

## Description

The Collaborative Online Notes App is a full-stack web application that combines:

-Python (FastAPI) as the backend API for secure data access and business logic.

-React as the responsive, interactive frontend for creating and editing notes in the browser.

-Supabase (PostgreSQL + built-in authentication + realtime features) as the database and user management system.


## Key Features

1. *User Authentication & Security*
Users can sign up and log in securely using Supabase Auth.

2. Create, Edit, and Delete Notes
Each user can create unlimited notes with a title, content, and optional tags.

3. Real-Time Collaboration
When a note is updated, all connected users see the changes instantly using Supabase’s realtime subscriptions.

4. Sharing Options
Notes can be marked as shared so other users can view them.

5. Persistent Cloud Storage
All notes are stored in Supabase’s PostgreSQL database and can be accessed from any device.


## collab-notes-app/
|
|---src/ #core application
|   |--logic.py #Business logic  and task
|   |--db.py    #For database Operations
|
|
|---api/        #backend API
|   |--main.py  # FastAPI endpoints
|
|
|---frontend/   #Frontend application
|   |--app.py   #Streamlit Web interface
|
|
|--requirements.txt     # installing python dependences
|
|
|--README.md    #python documentation
|
|
|-- .env     #Python Variables



## Quick Start

### Prerequisties

- Python 3.8 or higher
- A supabase account
- Git (push,clone)

### 1. Clone or Download the Project
# Option 1 : clone with Git
git clone <>

### Option 2: Install dependencies

# install all required Python packages 
pip install -r requirements.txt 

### 3.Set Up Supabase Database 

1.create a supabase project :


2.create the task Tables:

    -go to the sql Editor in your supabase dashboard 
    -run  this sql command:

``` 
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Notes table
CREATE TABLE notes (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    tags TEXT[],  -- PostgreSQL array type
    is_shared BOOLEAN DEFAULT FALSE,
    share_link VARCHAR(255)
);

```
## 4.Configure environment variables
1.Create a `.env` file in the project root

2.Add your supabase credentials to `.env`
SUPABASE_URL='your supabase_url'
SUPABASE_KEY='your supabase_key'

## 5.Run the application
streamlit run Frontend/app.py
The API is available at `http://localhost:8501`

## FastAPI Backend
cd api
python main.py
The API is available at `http://localhost:8000`

## How to use

## Technologies used

**Frontend**:Streamlit(Python Web framework)
**Backend**:FastAPI(Python REST API Framework)
**Database**:Supabase(Postgre-SQL based backend-as-a-service)
**Language**:Python 3.8+

## Key Components

1.src/db.py:Database operations(Handles all crud operations with supabase)
2.src/logic.py:Business logic(Handles task and processing)

## Troubleshooting

## Common Issues

1.**Module not found error**
-Make sure you have installed dependencies `pip install -r requirements.txt`
-Check that you're running commands from the correct directory

## Future Enhancements
Ideas for extending the project:

**User authentication**:Add user accounts  and login 
**Task Categories**:organization tasks by the subject or category
**Nofication**:Email or push notification for the due dates
**File attachment**:Attach files   to tasks
**Collboration**:Share tasks with your classmate




<!-- git clone repo link or branch name
git init
git add .(filename)
git commit -m "comment"
git push -->

