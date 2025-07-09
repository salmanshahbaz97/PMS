# Player Management System (PMS)

A modern, role-based Django application for managing sports teams, coaches, and players with a beautiful, responsive UI.

## 🏆 Features

### Role-Based Access Control
- **Admin**: Full system access, can manage all users, coaches, and players
- **Coach**: Can view and manage assigned players
- **Player**: Can view personal information and assigned coach

### Key Features
- ✨ Modern, responsive UI with Bootstrap 5
- 🔐 Secure authentication system
- 👥 User management with role-based permissions
- 🏃 Player profiles with detailed information
- 👨‍🏫 Coach management with player assignments
- 📊 Beautiful dashboards for each role
- 🎨 Custom styling with gradients and animations
- 📱 Mobile-friendly design

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd pms-latest
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main application: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/
   - Login page: http://127.0.0.1:8000/login/

## 📋 Usage Guide

### For Administrators

1. **Access Admin Panel**
   - Go to http://127.0.0.1:8000/admin/
   - Login with your superuser credentials

2. **Create Users**
   - Navigate to "Users" section
   - Click "Add User"
   - Fill in user details and assign appropriate role (Admin/Coach/Player)

3. **Create Coaches**
   - Navigate to "Coaches" section
   - Click "Add Coach"
   - Select a user with Coach role
   - Add specialization, experience, and bio

4. **Create Players**
   - Navigate to "Players" section
   - Click "Add Player"
   - Select a user with Player role
   - Add position, jersey number, and assign to a coach

5. **Assign Players to Coaches**
   - In the Players section, edit any player
   - Select a coach from the dropdown
   - Save changes

### For Coaches

1. **Login to System**
   - Go to http://127.0.0.1:8000/login/
   - Use your coach credentials

2. **View Dashboard**
   - See overview of assigned players
   - View player statistics and details

3. **Manage Players**
   - View list of assigned players
   - Access individual player profiles

### For Players

1. **Login to System**
   - Go to http://127.0.0.1:8000/login/
   - Use your player credentials

2. **View Personal Dashboard**
   - See personal information and stats
   - View assigned coach details

## 🏗️ Project Structure

```
pms-latest/
├── core/                    # Main application
│   ├── models.py           # Database models
│   ├── views.py            # View logic
│   ├── admin.py            # Admin interface
│   └── urls.py             # URL routing
├── templates/              # HTML templates
│   ├── base.html           # Base template
│   └── core/               # App-specific templates
├── static/                 # Static files
│   ├── css/                # Stylesheets
│   ├── js/                 # JavaScript files
│   └── images/             # Images
├── pms/                    # Project settings
│   ├── settings.py         # Django settings
│   └── urls.py             # Main URL configuration
├── requirements.txt        # Python dependencies
└── manage.py              # Django management script
```

## 🎨 UI/UX Features

### Design Principles
- **Modern & Clean**: Clean, professional design with modern UI elements
- **Responsive**: Works perfectly on desktop, tablet, and mobile devices
- **Accessible**: Follows accessibility best practices
- **Intuitive**: Easy-to-use interface with clear navigation

### Visual Elements
- **Gradient Backgrounds**: Beautiful gradient backgrounds throughout the app
- **Card-based Layout**: Information organized in clean, hoverable cards
- **Bootstrap Icons**: Consistent iconography using Bootstrap Icons
- **Smooth Animations**: Subtle animations and transitions
- **Color-coded Roles**: Different colors for different user roles

## 🔧 Customization

### Adding New Features
1. Create new models in `core/models.py`
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
- Keyboard shortcuts and animations

## 🛡️ Security Features

- **Role-based Access Control**: Users can only access features based on their role
- **Django Admin**: Secure admin interface for system management
- **Form Validation**: Client-side and server-side validation
- **CSRF Protection**: Built-in Django CSRF protection
- **Password Security**: Django's secure password hashing

## 📱 Responsive Design

The application is fully responsive and works on:
- **Desktop**: Full-featured interface with all options
- **Tablet**: Optimized layout for medium screens
- **Mobile**: Touch-friendly interface with simplified navigation

## 🚀 Deployment

### Production Setup
1. Set `DEBUG = False` in settings.py
2. Configure your database (PostgreSQL recommended)
3. Set up static file serving
4. Configure your web server (Nginx + Gunicorn recommended)

### Environment Variables
```bash
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=your-database-url
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues or have questions:
1. Check the documentation
2. Search existing issues
3. Create a new issue with detailed information

## 🎯 Roadmap

### Planned Features
- [ ] Training schedule management
- [ ] Performance tracking
- [ ] Team statistics
- [ ] Match scheduling
- [ ] Injury tracking
- [ ] Equipment management
- [ ] Financial tracking
- [ ] API endpoints
- [ ] Mobile app

### Technical Improvements
- [ ] Unit tests
- [ ] Integration tests
- [ ] Performance optimization
- [ ] Caching implementation
- [ ] API documentation
- [ ] Docker support

---

**Built with ❤️ using Django and Bootstrap 5** 