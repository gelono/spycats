# SpyCats Project

## Description
This is a FastAPI project utilizing PostgreSQL as the database and SQLAlchemy for ORM 
(Object-Relational Mapping). The API provides endpoints for CRUD operations to manage spy
cats, missions and targets.

## Getting Started

### Prerequisites
- Python 3.10+
- PostgreSQL
- Virtual Environment (recommended)

### Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/gelono/spycats.git
   cd spycats
   
2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # For Linux/Mac
    venv\Scripts\activate     # For Windows

3. Install dependencies:
    ```bash
   pip install -r requirements.txt
   
4. Configure the PostgreSQL database:
    ```bash
   CREATE DATABASE your_db_name;
    CREATE USER your_db_user WITH PASSWORD 'your_db_password';
    ALTER ROLE your_db_user SET client_encoding TO 'utf8';
    ALTER ROLE your_db_user SET default_transaction_isolation TO 'read committed';
    GRANT ALL PRIVILEGES ON DATABASE your_db_name TO your_db_user;

5. Update session.py and alembic.ini variables with your PostgreSQL database configuration:
SQLALCHEMY_DATABASE_URL = "postgresql://your_db_user:your_db_password@localhost/your_db_name"
sqlalchemy.url = postgresql://postgres:postgres@localhost/spycats


6. Create database tables and apply migrations using Alembic:
   ```bash
   alembic upgrade head
   
7. Run the FastAPI development server:
    ```bash
   uvicorn main:app --reload

The FastAPI server will be available at http://127.0.0.1:8000.


API Documentation
FastAPI automatically generates interactive API documentation. Visit the following URL to explore the available endpoints:

- Swagger UI: http://127.0.0.1:8000/docs

- ReDoc UI: http://127.0.0.1:8000/redoc

Notes
- This project uses SQLAlchemy as the ORM and Alembic for database migrations.
- Make sure to set up your PostgreSQL database and update the connection details in session.py and alembic.ini before running the application.