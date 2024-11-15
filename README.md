# Crisis Management System

A web-based application for organizations to efficiently manage emergencies, streamline incident reporting, and reduce response times through a centralized platform. This system facilitates communication between volunteers, organizations, and communities during crises.

## Features

- **User Registration and Authentication:** Users can register as volunteers or organizations, log in, and manage their profile.
- **Incident Reporting:** Users can report incidents, provide descriptions, attach images, and specify severity.
- **Profile Management:** Logged-in users can view their profiles and log out.
- **Carousel Display:** Home page features a carousel section to showcase images or information.
- **Contact Form and Google Maps Integration:** Users can reach out via a contact form and locate the organization's address through an embedded map.

## Prerequisites

- Python 3.x
- Django 4.x
- Virtual environment (recommended)

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

## License

This project is licensed under the MIT License.

## Contributing

1. Fork the repository
2. Create a new branch for your feature: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add new feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request