# Regression App 🚀

A full-stack **machine learning regression platform** that allows users to upload datasets, run regression experiments, and visualize results.  
The project is designed with a **cloud-ready architecture** using AWS services and Docker.

---

## 🔍 Project Overview

This application allows users to:
- Register & authenticate
- Upload datasets (CSV / Excel)
- Select regression algorithms
- Run experiments
- View metrics and plots (RMSE, R², residuals, etc.)
- Download experiment artifacts

The backend is built with **FastAPI** and **PostgreSQL (AWS RDS)**, while the frontend uses **React + Vite**.  
The system is developed locally first and then deployed using **Docker, ECS, S3, and CloudFront**.

---

## 🧱 Architecture 

Frontend (React + Vite)
|
| HTTPS
v
Backend (FastAPI + Docker)
|
v
PostgreSQL (AWS RDS)
|
v
S3 (Dataset & Artifacts Storage)


---

## 🛠 Tech Stack

### Backend
- Python 3.11
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL (AWS RDS)
- scikit-learn
- Matplotlib
- JWT Authentication

### Frontend
- React
- Vite
- Tailwind CSS
- Axios

### Cloud & DevOps
- AWS RDS (PostgreSQL)
- AWS S3
- AWS ECS (Fargate)
- AWS CloudFront
- Docker
- GitHub

---

## 📂 Project Structure

regression-app/
│
├── backend/
│ ├── app/
│ ├── migrations/
│ ├── requirements.txt
│ └── main.py
│
├── frontend/
│ ├── src/
│ ├── public/
│ └── vite.config.ts
│
├── .gitignore
└── README.md


---

## ⚙️ Local Development 

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL (AWS RDS)
- Git

### Backend Setup

cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

### Create .env inside backend/:

DATABASE_URL=postgresql://user:password@host:5432/dbname
JWT_SECRET=your_secret_key

### Run migrations:

alembic upgrade head

### Start backend:

uvicorn app.main:app --reload

### Frontend Setup

cd frontend
npm install
npm run dev

---

## Features Implemented

User authentication (JWT)

Dataset upload

Regression experiment execution

Metrics & plots generation

Experiment history

Secure database connection