# Player Management System - Deployment Guide

## 🚀 Quick Deploy to Render (Completely Free - No Credit Card Required)

### Prerequisites
- GitHub account
- Render account (completely free, no credit card required)

### Step 1: Prepare Your Project

1. **Install deployment dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Collect static files:**
   ```bash
   python manage.py collectstatic --noinput
   ```

3. **Create a `.env` file for local development:**
   ```bash
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   ALLOWED_HOSTS=localhost,127.0.0.1
   DATABASE_URL=sqlite:///db.sqlite3
   ```

### Step 2: Deploy to Render

1. **Go to [Render.com](https://render.com)**
2. **Sign up/Login with GitHub (no credit card required)**
3. **Click "New +" → "Web Service"**
4. **Connect your GitHub repository**
5. **Render will automatically detect Django and deploy**

### Step 3: Configure Environment Variables

In Render dashboard, add these environment variables:

```
DEBUG=False
SECRET_KEY=your-production-secret-key-here
ALLOWED_HOSTS=your-app-name.onrender.com
DATABASE_URL=postgresql://... (Render will provide this)
```

### Step 4: Run Migrations

In Render dashboard:
1. Go to your web service
2. Click on "Environment" tab
3. Add a new environment variable:
   - **Key:** `BUILD_COMMAND`
   - **Value:** `pip install -r requirements.txt && python manage.py collectstatic --noinput`
4. Add another variable:
   - **Key:** `START_COMMAND`
   - **Value:** `gunicorn pms.wsgi:application`

### Step 5: Create Superuser

After deployment, you can create a superuser by:
1. Go to your web service in Render
2. Click on "Shell" tab
3. Run: `python manage.py migrate`
4. Run: `python manage.py createsuperuser`
5. Follow the prompts to create admin user

## 🌐 Alternative Free Hosting Options

### Render (Free Tier) - RECOMMENDED
- **Pros:** Easy deployment, PostgreSQL included, completely free
- **Cons:** Sleeps after 15 minutes inactivity (wakes up on first request)
- **Deploy:** Connect GitHub repo, auto-deploys
- **No credit card required!**

### PythonAnywhere (Free Tier) - ALTERNATIVE
- **Pros:** Python-focused, includes database, very reliable
- **Cons:** Limited resources, no custom domains on free tier
- **Deploy:** Upload files, configure WSGI
- **No credit card required!**

### Vercel (Limited)
- **Pros:** Fast, easy deployment
- **Cons:** Limited backend support
- **Best for:** Frontend-heavy apps

## 🔧 Production Checklist

### Security
- [ ] Set `DEBUG=False`
- [ ] Use strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use HTTPS (automatic on Railway/Render)

### Database
- [ ] Use PostgreSQL (not SQLite)
- [ ] Run migrations
- [ ] Create superuser
- [ ] Backup strategy

### Static Files
- [ ] Run `collectstatic`
- [ ] Configure WhiteNoise
- [ ] Test static file serving

### Performance
- [ ] Enable database connection pooling
- [ ] Configure caching (Redis recommended)
- [ ] Optimize database queries

## 📝 Environment Variables

### Required
```
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgresql://...
```

### Optional
```
RAILWAY_RUN_MIGRATIONS=python manage.py migrate
RAILWAY_CREATE_SUPERUSER=python manage.py createsuperuser --noinput
```

## 🐛 Troubleshooting

### Common Issues

1. **Static files not loading:**
   - Run `python manage.py collectstatic`
   - Check WhiteNoise configuration

2. **Database connection errors:**
   - Verify `DATABASE_URL` format
   - Check database credentials

3. **500 errors:**
   - Check logs in hosting platform
   - Verify environment variables
   - Test locally with production settings

### Debug Mode
For debugging, temporarily set:
```
DEBUG=True
```

## 🔄 Continuous Deployment

### GitHub Actions (Optional)
Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Railway
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Railway
        uses: railway/deploy@v1
        with:
          railway_token: ${{ secrets.RAILWAY_TOKEN }}
```

## 📊 Monitoring

### Railway Dashboard
- View logs in real-time
- Monitor resource usage
- Check deployment status

### Django Admin
- Access at `your-domain.com/admin/`
- Monitor user activity
- Manage data

## 🎉 Success!

Your Player Management System is now live! Share the URL with your team.

### Next Steps
1. Test all functionality
2. Create user accounts
3. Set up regular backups
4. Monitor performance
5. Plan for scaling

---

**Need help?** Check the hosting platform's documentation or Django deployment guides. 