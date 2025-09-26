# HRMS Vercel Deployment Guide

## ❌ Current Status: NOT DEPLOYMENT READY

Your Django HRMS application has several critical issues that need to be fixed before deploying to Vercel.

## 🚨 Critical Issues Found:

### 1. **Hardcoded URLs Fixed** ✅
- Fixed hardcoded localhost URLs in backend upload scripts
- Fixed hardcoded URLs in Django views (`auth.py`)
- Updated frontend components to use dynamic API configuration
- Added environment variable support for `BACKEND_URL`

### 2. **Missing Vercel Configuration** ✅
- Created `vercel.json` configuration file for serverless deployment

### 3. **Environment Variables Setup** ✅
- Added `BACKEND_URL` to Django settings
- Updated `.env` file with production URLs
- Created frontend environment files (`.env.local`, `.env.production`)

## 🔧 Remaining Issues to Fix:

### 1. **Django Static Files Configuration**
Your Django app needs proper static file handling for Vercel:

```python
# Add to settings.py
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# For Vercel deployment
if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### 2. **Database Configuration for Production**
Update your database settings for production:

```python
# In settings.py, add database URL support
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default=f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}@{config('DB_HOST')}:{config('DB_PORT')}/{config('DB_NAME')}")
    )
}
```

### 3. **CORS Configuration for Vercel**
Your CORS settings need to support Vercel domains:

```python
# Update CORS_ALLOWED_ORIGINS in .env
CORS_ALLOWED_ORIGINS=https://your-frontend-app.vercel.app,https://your-backend-api.vercel.app
```

### 4. **Security Settings for Production**
Update security settings for HTTPS:

```python
# In settings.py for production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    CSRF_TRUSTED_ORIGINS = ['https://your-app.vercel.app']
```

## 📝 Deployment Steps:

### Step 1: Install Required Dependencies
Add to your `requirements.txt`:
```
dj-database-url==2.1.0
whitenoise==6.6.0
```

### Step 2: Update Environment Variables
Create a `.env.production` file:
```bash
DEBUG=False
SECRET_KEY=your-production-secret-key
DATABASE_URL=your-neon-database-url
FRONTEND_URL=https://your-frontend.vercel.app
BACKEND_URL=https://your-backend.vercel.app
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
ALLOWED_HOSTS=your-backend.vercel.app,.vercel.app
```

### Step 3: Vercel Project Setup
1. Create separate Vercel projects for frontend and backend
2. Deploy backend first, then frontend
3. Update frontend environment variables with backend URL

### Step 4: Database Migrations
Run migrations after deployment:
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

## ⚠️ Important Notes:

1. **Separate Deployments**: Deploy backend and frontend as separate Vercel projects
2. **Environment Variables**: Set all environment variables in Vercel dashboard
3. **Domain Configuration**: Update CORS and ALLOWED_HOSTS after getting Vercel URLs
4. **Static Files**: Ensure static files are properly collected and served
5. **Database**: Make sure your Neon database is accessible from Vercel

## 🎯 Next Steps:

1. Fix the remaining issues listed above
2. Test locally with production-like settings
3. Deploy backend to Vercel first
4. Deploy frontend with backend URL
5. Update CORS settings with actual domains
6. Test the deployed application thoroughly

## 📞 Questions to Ask:

1. Do you want to deploy backend and frontend as separate Vercel projects?
2. Do you have access to your Neon database from external sources?
3. Should we set up a staging environment first?
4. Do you need help with the actual deployment process?

The main issues have been addressed, but you'll need to complete the remaining configuration steps before deployment.