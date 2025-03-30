# Django Project Setup Guide

### Clone the repository
```bash
git clone https://github.com/Sahiiil1406/BCC

# Navigate to folder BCC
cd BCC
```

### Create .env file

```bash
cp .env.example .env
```
- Fill in the required variables in the .env file
<br>
- <b>This is required for the database connection using PostgreSQL

### Initial Setup

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install Django
pip install -r requirements.txt
```



### Database Migrations

```bash
# Create migrations for all apps
python manage.py makemigrations

# Apply all migrations
python manage.py migrate

```

### Running the Server

```bash
# Start the development server
python manage.py runserver
```

Your Django project will be available at: http://127.0.0.1:8000/api
