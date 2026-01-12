# Customer Insights & Business Report Portal

A role-based web application for managing customer data analysis and delivering business reports. Built with FastAPI (Backend) and Vanilla JS/HTML/CSS (Frontend).

## 🚀 Features

- **Role-Based Access**: Admin (Business Analyst) and Client (Customer) roles.
- **Secure Authentication**: JWT-based login and registration.
- **File Uploads**: Clients can upload data files (PDF, Excel, Docx) to Supabase Storage.
- **Report Management**: Admins can review uploads and send back analyzed reports (PDF).
- **Notifications**: Clients receive real-time updates when reports are ready.
- **Public Landing Page**: Modern, glassmorphism-styled landing page for new inquiries.

## 🛠 Tech Stack

- **Frontend**: HTML5, CSS3 (Glassmorphism), Vanilla JavaScript.
- **Backend**: Python, FastAPI, SQLAlchemy.
- **Database**: PostgreSQL (Supabase).
- **Storage**: Supabase Storage.
- **Deployment**: Netlify (Frontend) + Render (Backend).

## 🏃‍♂️ Local Development Setup

### Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure Environment Variables:
   - Rename `.env.example` to `.env`.
   - Update `DATABASE_URL` (Supabase Connection String).
   - Update `SUPABASE_URL` and `SUPABASE_KEY`.
   - Set a `SECRET_KEY`.
5. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```
   The API will be available at `http://localhost:8000`.

### Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Serve the directory using any static server (e.g., Live Server in VS Code):
   - Access `http://localhost:5500/index.html` (or your local port).
3. **Important**: If your backend is not running on `localhost:8000`, update `assets/js/api.js` with the correct `API_URL`.

## ☁️ Deployment Guide

### 1. Database (Supabase)
- Create a new project on Supabase.
- Run the provided SQL migration (tables are auto-created by SQLAlchemy on first run).
- Create a storage bucket named `uploads` and `reports`. Make them public or configure policies.

### 2. Backend (Render)
- Connect your repository to Render.
- Create a new **Web Service**.
- **Root Directory**: `backend`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port 10000`
- **Environment Variables**: Add all variables from your `.env` file.

### 3. Frontend (Netlify)
- Connect your repository to Netlify.
- **Base Directory**: `frontend`
- **Publish Directory**: `frontend` (or leave empty if Base is set).
- **Post-Deploy**: Update `assets/js/api.js` with your production Render backend URL.

## 🔒 Security Notes
- JWT tokens are stored in LocalStorage.
- Ensure `SECRET_KEY` is strong and kept secret.
- Admin registration is currently open for demo purposes; restrict in production.
