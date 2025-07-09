# Player Management System - Quick Setup Guide

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 3: Create Superuser (Admin)
```bash
python manage.py createsuperuser
```
Follow the prompts to create your admin account.

### Step 4: Run the Development Server
```bash
python manage.py runserver
```

### Step 5: Access the Application
- **Main Application**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Login Page**: http://127.0.0.1:8000/login/

## 👥 User Roles & Permissions

### Admin
- Full system access
- Can create/edit/delete users, coaches, and players
- Can assign players to coaches
- Access to admin panel

### Coach
- Can view assigned players
- Can view player details
- Limited to their assigned players only

### Player
- Can view personal information
- Can view assigned coach details
- Limited to their own profile

## 🎯 Quick Start Workflow

### 1. Admin Setup (First Time)
1. Login to admin panel: http://127.0.0.1:8000/admin/
2. Create users with different roles:
   - Go to "Users" → "Add User"
   - Set role to "Coach" or "Player"
3. Create Coach profiles:
   - Go to "Coaches" → "Add Coach"
   - Select a user with Coach role
4. Create Player profiles:
   - Go to "Players" → "Add Player"
   - Select a user with Player role
   - Assign to a coach

### 2. Coach Login
1. Go to: http://127.0.0.1:8000/login/
2. Use coach credentials
3. View assigned players and manage them

### 3. Player Login
1. Go to: http://127.0.0.1:8000/login/
2. Use player credentials
3. View personal information and assigned coach

## 🎨 Features Implemented

### ✅ Core Features
- [x] Custom User Model with Role-based Authentication
- [x] Coach and Player Models
- [x] Admin Interface for User Management
- [x] Role-based Dashboards
- [x] Beautiful UI with Bootstrap 5
- [x] Responsive Design
- [x] Search and Filter Functionality
- [x] Profile Management
- [x] Player-Coach Assignment System

### ✅ UI/UX Features
- [x] Modern, gradient-based design
- [x] Card-based layouts
- [x] Bootstrap Icons
- [x] Hover effects and animations
- [x] Mobile-responsive design
- [x] Custom CSS styling
- [x] Interactive JavaScript features

### ✅ Security Features
- [x] Role-based access control
- [x] Django admin security
- [x] CSRF protection
- [x] Secure password handling

## 📁 Project Structure

```
pms-latest/
├── core/                    # Main application
│   ├── models.py           # User, Coach, Player models
│   ├── views.py            # View logic and permissions
│   ├── admin.py            # Admin interface configuration
│   └── urls.py             # URL routing
├── templates/              # HTML templates
│   ├── base.html           # Base template with navigation
│   └── core/               # App-specific templates
│       ├── login.html      # Login page
│       ├── admin_dashboard.html
│       ├── coach_dashboard.html
│       ├── player_dashboard.html
│       ├── player_list.html
│       ├── player_detail.html
│       ├── coach_list.html
│       └── *_profile.html  # Profile templates
├── static/                 # Static files
│   ├── css/style.css       # Custom styling
│   └── js/main.js          # JavaScript functionality
├── pms/                    # Project settings
│   ├── settings.py         # Django configuration
│   └── urls.py             # Main URL configuration
├── requirements.txt        # Python dependencies
├── README.md              # Comprehensive documentation
└── manage.py              # Django management script
```

## 🔧 Customization

### Adding New Features
1. Create models in `core/models.py`
2. Add views in `core/views.py`
3. Create templates in `templates/core/`
4. Update URL patterns in `core/urls.py`

### Styling
- Main styles: `static/css/style.css`
- Bootstrap 5 for responsive design
- Custom gradients and animations

### JavaScript
- Main script: `static/js/main.js`
- Interactive features and form validation

## 🐛 Troubleshooting

### Common Issues

1. **Migration Errors**
   ```bash
   python manage.py makemigrations --empty core
   python manage.py migrate
   ```

2. **Static Files Not Loading**
   ```bash
   python manage.py collectstatic
   ```

3. **Database Issues**
   ```bash
   python manage.py flush  # Clear database
   python manage.py migrate
   ```

4. **Permission Issues**
   - Ensure user has correct role assigned
   - Check admin panel for user permissions

## 📞 Support

If you encounter any issues:
1. Check the README.md for detailed documentation
2. Verify all dependencies are installed
3. Ensure database migrations are complete
4. Check Django debug output for error messages

## 🎯 Next Steps

### Planned Features
- [ ] Training schedule management
- [ ] Performance tracking
- [ ] Team statistics
- [ ] Match scheduling
- [ ] Injury tracking
- [ ] Equipment management
- [ ] API endpoints
- [ ] Mobile app

---

**🎉 Congratulations! Your Player Management System is ready to use!** 