# Regression App

A full-stack web application for running regression experiments. The backend is built with **FastAPI**, PostgreSQL (RDS), and AWS services like S3. The frontend is built using **Vite/React** and deployed on **AWS Amplify**.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Setup Instructions](#setup-instructions)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Environment Variables](#environment-variables)
- [Deployment](#deployment)
- [Connecting Frontend & Backend](#connecting-frontend--backend)
- [Requirements](#requirements)


---

## Project Overview

- Backend hosted on **AWS EC2** with **Elastic IP**.
- Database hosted on **AWS RDS (PostgreSQL)**.
- File storage using **AWS S3**.
- Frontend hosted on **AWS Amplify** and connected to the backend via API.
- Implements authentication using JWT.
- Run regression experiments, manage datasets, and store results.

---

## Tech Stack

**Backend:** FastAPI, Uvicorn, PostgreSQL, SQLAlchemy, Alembic, Boto3, Pydantic  
**Frontend:** React, Vite, AWS Amplify  
**Cloud Services:** AWS EC2, RDS, S3, Amplify  

---

## Setup Instructions

### Backend Setup

1. SSH into your EC2 instance:

```bash
ssh -i path/to/regression-app-key.pem ubuntu@<EC2_PUBLIC_IP>

2. Navigate to backend folder:

cd ~/regression-app/backend


3. Create and activate virtual environment:

python3 -m venv .venv
source .venv/bin/activate


4. Install dependencies:

pip install -r requirements.txt


5. Run the backend server:

uvicorn app.main:app --host 0.0.0.0 --port 8000


Backend should now be accessible at http://<EC2_PUBLIC_IP>:8000.

---

##  Frontend Setup

1. Navigate to the frontend directory:

cd ~/regression-app/frontend


2. Install dependencies:

npm install


3. Start the development server:

npm run dev

---

## Environment Variables

Create a `.env` file in `backend/` with the following:

DATABASE_URL=postgresql://<user>:<password>@<rds-endpoint>:5432/<db_name>
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1
S3_BUCKET_NAME=your_bucket_name
JWT_SECRET_KEY=your_secret_key

---

## Deployment

### Backend
- Deployed on AWS EC2 (Ubuntu)
- Uses Elastic IP for stable access
- FastAPI served via Uvicorn

### Database
- PostgreSQL hosted on AWS RDS
- Connected securely via security groups

### Frontend
- Built using Vite + React
- Deployed on AWS Amplify

---

## Connecting Frontend & Backend

The frontend communicates with the backend via REST APIs.

Set the backend API URL in the frontend environment file:

VITE_API_BASE_URL=http://<EC2_PUBLIC_IP>:8000

After updating, redeploy the frontend on AWS Amplify.

---

## Requirements

Python 3.9+

Node.js 18+

AWS account (Free Tier compatible)