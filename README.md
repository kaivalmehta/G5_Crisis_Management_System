# G5_Crisis_Management_System

# Django Project Setup

This guide will help you set up and run the Django project locally on your machine.

## Prerequisites

Make sure you have the following installed on your machine:

- Python 3.x
- pip (Python package manager)
- Virtualenv (optional, but recommended)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd <your-project-directory>
```

### 2. Create and Activate a Virtual Environment (optional, but recommended)

Creating a virtual environment isolates the project dependencies from your global Python installation.

#### For Unix/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### For Windows:
```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies

Make sure to install all required dependencies by running the following command:

```bash
pip install -r requirements.txt
```

### 4. Set up Environment Variables

Create a `.env` file in the project root and add your environment-specific variables. Example:

```bash
SECRET_KEY='your-django-secret-key'
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=sqlite:///db.sqlite3  # Or your preferred database
```

### 5. Apply Migrations

To set up your database schema, run the following migrations command:

```bash
python manage.py migrate
```

### 6. Create a Superuser (for Admin Access)

Create a superuser to access Django's admin panel:

```bash
python manage.py createsuperuser
```

### 7. Run the Development Server

You can now run the Django development server:

```bash
python manage.py runserver
```

Visit [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) to access the Django Admin panel.

## Testing

To run tests for the project, you can use the following command:

```bash
python manage.py test
```

## Common Issues

### Model class doesn't declare an explicit app_label
If you see the following error:

```
RuntimeError: Model class django.contrib.sessions.models.Session doesn't declare an explicit app_label and isn't in an application in INSTALLED_APPS.
```

Make sure you have `django.contrib.sessions` included in the `INSTALLED_APPS` list in your `settings.py`:

```python
INSTALLED_APPS = [
    # Other apps...
    'django.contrib.sessions',
]
```

## Deployment

For deployment, make sure to configure:

- `DEBUG = False`
- Use a production-ready database like PostgreSQL
- Set proper `ALLOWED_HOSTS`
- Use `whitenoise` for serving static files
- Set up environment variables for secret keys, database credentials, etc.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
