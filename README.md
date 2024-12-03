# Crisis Management System

Imagine you’re in the midst of a natural disaster or a local emergency. You see people in need, organizations wanting to help, and volunteers ready to act—but there’s no system to connect them all effectively. That’s where KarunaCMS steps in.

KarunaCMS is a platform that bridges the gap between citizens, volunteers, and organizations to respond to crises faster and more efficiently. Whether it’s reporting an incident, coordinating resources, or volunteering to help, KarunaCMS empowers communities to take meaningful action during critical times.

## Features

- **User Registration & Authentication:**
  - Register users as volunteers or organizations.
  - Password validation, including length and confirmation checks.
  - Login and logout functionality.

- **Profile Management:**
  - Separate profiles for volunteers and organizations.
  - Edit profile options tailored to their respective attributes.

- **Resource Management:**
  - Organizations can manage resources, including adding and deleting them.

- **Volunteer-Organization Interaction:**
  - Organizations can view their volunteers.
  - Tasks can be created and assigned to volunteers.

- **Task Management:**
  - Tasks associated with crises can be created, viewed, updated, and deleted.
  - Volunteers can accept tasks and mark them as done.

## Project Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/crisis-management-system.git
cd crisis-management-system
```

### 2. Set Up a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Database

Apply migrations to set up the database schema.

```bash
python manage.py migrate
```

### 5. Create a Superuser

Create a superuser account to access the Django admin panel.

```bash
python manage.py createsuperuser
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

Access the application at `http://127.0.0.1:8000`.

## Project Structure

- **`base.html`** - Base template that includes navigation and footer.
- **`home.html`** - Home page with a carousel, about section, report incident form, and contact form.
- **`register.html`** - Registration form allowing users to sign up as volunteers or organizations.
- **`login.html`** - Login form with a link to the registration page.
- **`profile.html`** - Profile page with a logout button.
- **`urls.py`** - URL routing configuration for all views.
- **`views.py`** - Contains view functions for handling requests, including login, register, profile, etc.
- **`models.py`** - Database models (if applicable, e.g., for users, incidents, etc.).
- **`forms.py`** - Django forms for handling registration and login.
- **`static/`** - Directory for static files, such as CSS, JavaScript, and images.