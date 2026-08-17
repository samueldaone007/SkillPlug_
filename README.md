# SkillPlug - Nigerian Student Skills Marketplace

A production-ready MVP web application that connects Nigerian university students with clients who need affordable digital services. Built with Django, TailwindCSS, and PostgreSQL.

## Features

### Core Platform
- **User Authentication** - Sign up, login, logout, password reset with email
- **Student Profiles** - Full profile with school, department, bio, skills, WhatsApp
- **Verification System** - Student ID verification with admin-approved badges
- **Portfolio System** - Upload project images with titles and descriptions
- **Job Board** - Post jobs, browse listings, apply with messages
- **WhatsApp Integration** - One-click contact via WhatsApp click-to-chat
- **Reviews & Ratings** - 5-star rating system with comments
- **Saved Freelancers** - Bookmark favorite students
- **Dark Mode** - Toggle between light and dark themes
- **HTMX Live Search** - Real-time freelancer search without page reloads
- **Responsive Design** - Mobile-first with bottom navigation

### Admin Features
- Full Django Admin integration
- Bulk verify/unverify students
- Moderate job posts and applications
- Manage users, skills, and reviews

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Django 5.0 | Backend framework |
| PostgreSQL | Database |
| TailwindCSS | Styling (via CDN) |
| HTMX | Interactive features |
| django-allauth | Authentication |
| django-crispy-forms | Form rendering |
| Pillow | Image processing |
| WhiteNoise | Static file serving |
| Gunicorn | WSGI server |

## Project Structure

```
skillplug/
├── apps/
│   ├── accounts/          # Custom user model, auth, profiles
│   ├── marketplace/       # Freelancer browsing, portfolio, home
│   ├── jobs/              # Job postings and applications
│   └── reviews/           # Ratings and reviews
├── templates/             # All HTML templates
│   ├── accounts/          # Auth and profile templates
│   ├── marketplace/       # Home, freelancer list
│   ├── jobs/              # Job board templates
│   ├── reviews/           # Review form
│   └── partials/          # Reusable components
├── static/                # CSS, JS, images
├── media/                 # User uploads
├── skillplug/             # Project settings
├── manage.py
├── requirements.txt
└── .env.example
```

## Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL 13+
- Virtual environment tool (venv or virtualenv)

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd skillplug

# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup

```bash
# Create PostgreSQL database
createdb skillplug_db

# Copy environment file
cp .env.example .env

# Edit .env with your database credentials
# DB_NAME=skillplug_db
# DB_USER=postgres
# DB_PASSWORD=your_password
# DB_HOST=localhost
# DB_PORT=5432
```

### 3. Run Migrations and Seed Data

```bash
# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Seed sample data (optional)
python manage.py seed_data
```

### 4. Run Development Server

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/

### Admin Panel

Visit http://127.0.0.1:8000/admin/ to manage users, verify students, and moderate content.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Debug mode | `True` |
| `SECRET_KEY` | Django secret key | (required in production) |
| `DB_NAME` | PostgreSQL database name | `skillplug_db` |
| `DB_USER` | PostgreSQL username | `postgres` |
| `DB_PASSWORD` | PostgreSQL password | `password` |
| `DB_HOST` | PostgreSQL host | `localhost` |
| `DB_PORT` | PostgreSQL port | `5432` |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `localhost,127.0.0.1` |
| `EMAIL_HOST_USER` | SMTP email | (optional) |
| `EMAIL_HOST_PASSWORD` | SMTP password | (optional) |

## Deployment Guide

### Deploying to Railway/Render/Heroku

1. **Create a PostgreSQL database** on your chosen platform
2. **Set environment variables** from the table above
3. **Deploy code** via Git integration
4. **Run migrations**: `python manage.py migrate`
5. **Create superuser**: `python manage.py createsuperuser`
6. **Collect static files**: `python manage.py collectstatic --noinput`

### Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Generate new `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up email for password reset
- [ ] Configure static file storage (AWS S3/Cloudinary)
- [ ] Enable SSL/HTTPS
- [ ] Set up monitoring and logging

### Sample Data Credentials

After running `python manage.py seed_data`, you can log in with:

| Username | Email | Password |
|----------|-------|----------|
| ademola_dev | ademola@unilag.edu.ng | password123 |
| chioma_designs | chioma@oau.edu.ng | password123 |
| tunde_writes | tunde@ui.edu.ng | password123 |
| fatima_apps | fatima@abu.edu.ng | password123 |
| sarah_client | sarah@gmail.com | password123 |

## API Endpoints / URL Routes

| URL | Description | Auth Required |
|-----|-------------|---------------|
| `/` | Home page | No |
| `/accounts/signup/` | Registration | No |
| `/accounts/login/` | Sign in | No |
| `/accounts/logout/` | Sign out | Yes |
| `/accounts/password-reset/` | Password reset | No |
| `/accounts/profile/create/` | Complete profile | Yes |
| `/accounts/profile/edit/` | Edit profile | Yes |
| `/accounts/dashboard/` | User dashboard | Yes |
| `/accounts/saved/` | Saved freelancers | Yes |
| `/accounts/@username/` | Public profile | No |
| `/marketplace/freelancers/` | Browse freelancers | No |
| `/marketplace/freelancers/search/` | HTMX search | No |
| `/marketplace/portfolio/add/` | Add portfolio item | Yes |
| `/jobs/` | Job board | No |
| `/jobs/post/` | Post a job | Yes |
| `/jobs/<id>/` | Job detail | No |
| `/jobs/<id>/apply/` | Apply for job | Yes |
| `/reviews/freelancer/<username>/review/` | Leave review | Yes |
| `/admin/` | Django admin | Staff only |

## Mobile Optimizations

- **Bottom navigation bar** for authenticated users
- **Touch-friendly** buttons and inputs
- **Responsive cards** that stack on small screens
- **Optimized images** with lazy loading
- **Fast-loading** with minimal JavaScript
- **WhatsApp integration** for mobile-first communication

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Support

For questions or support, please open an issue on the repository or contact the maintainers.

---

Built with care for Nigerian students. Connect, create, and earn with SkillPlug!
