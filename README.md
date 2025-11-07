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


