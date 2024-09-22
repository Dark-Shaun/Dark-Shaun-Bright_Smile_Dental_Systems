# Dental Management System

A comprehensive web application for managing dental clinics, appointments, and patient records.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Database Setup](#database-setup)
5. [Running the Application](#running-the-application)
6. [Usage](#usage)
7. [Running Tests](#running-tests)
8. [Troubleshooting](#troubleshooting)

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- PostgreSQL 12 or higher

## Installation

1. Install PostgreSQL:
   - On Ubuntu: `sudo apt-get update && sudo apt-get install postgresql postgresql-contrib`
   - On macOS (using Homebrew): `brew install postgresql`
   - On Windows: Download and install from the [official PostgreSQL website](https://www.postgresql.org/download/windows/)

2. Start the PostgreSQL service:
   - On Ubuntu: `sudo service postgresql start`
   - On macOS: `brew services start postgresql`
   - On Windows: PostgreSQL should start automatically after installation

3. Clone the repository:
   ```
   git clone https://github.com/Dark-Shaun/Dark-Shaun-Bright_Smile_Dental_Systems.git
   cd dental-management-system
   ```

4. Create a virtual environment:
   ```
   python -m venv venv
   ```

5. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS and Linux: `source venv/bin/activate`

6. Install the required packages:
   pip install -r requirements.txt
   ```

## Configuration

1. Create a `.env` file in the project root directory:
   ```
   SECRET_KEY=your_secret_key_here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   # DB_NAME=dental_db --Uncomments while performing unit testing
   DB_USER=your_postgres_user
   DB_PASSWORD=your_postgres_password
   DB_HOST=localhost
   DB_PORT=5432
   ```

   Replace `your_secret_key_here`, `your_postgres_user`, and `your_postgres_password` with appropriate values.

2. Ensure the database settings in `dental_management_system/settings.py` are using the environment variables:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': os.getenv('DB_NAME'),
           'USER': os.getenv('DB_USER'),
           'PASSWORD': os.getenv('DB_PASSWORD'),
           'HOST': os.getenv('DB_HOST'),
           'PORT': os.getenv('DB_PORT'),
       }
   }
   ```

## Database Setup

1. Create the database:
   ```
   python manage.py dbshell
   ```
   In the PostgreSQL shell that opens, run:
   ```sql
   CREATE DATABASE dental_db;
   \q
   ```

2. Apply migrations to set up the database schema:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

3. Create a superuser (you'll use this to access the admin panel):
   ```
   python manage.py createsuperuser
   ```
   Follow the prompts to create your superuser account.

## Running the Application

1. Start the development server:
   ```
   python manage.py runserver
   ```

2. Open a web browser and go to `http://127.0.0.1:8000/`

## Usage

1. Log in using your superuser credentials.

2. Use the admin panel (`http://127.0.0.1:8000/admin/`) to:
   - Add clinics
   - Add doctors and their specialties
   - Add procedures
   - Check out the appointments, clinics, doctors, and procedures
   - Check out the database

3. From the main application:
   - Manage patients
   - Schedule appointments
   - View and update patient records
   - Add Visit
   - Schedule Appointment

## Running Unit Tests

To run the test suite:
- To Run Unit Tests: `python manage.py test`

## Troubleshooting

- If you encounter any issues with database migrations, try:
  ```
  python manage.py makemigrations
  python manage.py migrate
  ```

- For any package-related issues, ensure your virtual environment is activated and packages are up-to-date:
  ```
  pip install --upgrade -r requirements.txt
  ```

- If you're having trouble with the superuser login, you can create a new superuser or reset the password using:
  ```
  python manage.py changepassword <username>
  ```

- If you're having issues connecting to the PostgreSQL database, ensure the service is running and the credentials in your `.env` file are correct.

For any other issues, please open an issue on the GitHub repository.
