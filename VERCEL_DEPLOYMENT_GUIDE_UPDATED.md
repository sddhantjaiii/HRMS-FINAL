# Vercel Deployment Guide - UPDATED SOLUTION

## ✅ Issue Resolution
**Problem**: Root-level `vercel.json` was causing monorepo build failures:
```
sh: line 1: cd: frontend: No such file or directory
Error: Command "cd frontend && npm install && cd ../backend && pip install -r requirements.txt" exited with 1
```

**Solution**: 
1. ✅ **Removed root `vercel.json`** - No longer trying to build both projects together
2. ✅ **Fixed frontend `index.html`** - Changed `/src/main.tsx` to `./src/main.tsx` 
3. ✅ **Backend database connection fixed** - Added proper Neon PostgreSQL configuration
4. ✅ **Separate project deployment** - Frontend and backend as individual Vercel projects

## 🚀 Deployment Steps

### Step 1: Deploy Backend (Django API)

1. **Create New Vercel Project**
   - Go to Vercel Dashboard → New Project
   - Import from Git: `HRMS-FINAL` repository
   
2. **Configure Backend Settings**:
   - **Framework Preset**: Other
   - **Root Directory**: `backend`
   - **Build Command**: (leave empty - handled by vercel.json)
   - **Output Directory**: (leave empty)
   - **Install Command**: (leave empty - handled by vercel.json)

3. **Add Environment Variables**:
   ```
   DJANGO_SETTINGS_MODULE=dashboard.settings
   PYTHONPATH=.
   DJANGO_USE_LIGHTWEIGHT=true
   DATABASE_URL=postgresql://neondb_owner:npg_kiW2lJnVcsu8@ep-lingering-block-a1olkbv3-pooler.ap-southeast-1.aws.neon.tech:5432/neondb?sslmode=require
   DB_NAME=neondb
   DB_USER=neondb_owner
   DB_PASSWORD=npg_kiW2lJnVcsu8
   DB_HOST=ep-lingering-block-a1olkbv3-pooler.ap-southeast-1.aws.neon.tech
   DB_PORT=5432
   DEBUG=False
   SECRET_KEY=your-super-secret-key-here-change-in-production-hrms-2025
   ```

4. **Deploy Backend**

### Step 2: Deploy Frontend (React App)

1. **Create Another Vercel Project**
   - New Project → Import same `HRMS-FINAL` repository
   
2. **Configure Frontend Settings**:
   - **Framework Preset**: Vite (auto-detected)
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (auto-detected)
   - **Output Directory**: `dist` (auto-detected)
   - **Install Command**: `npm install` (auto-detected)

3. **Add Environment Variables**:
   ```
   VITE_BACKEND_URL=https://your-backend-app.vercel.app
   ```
   *(Replace with actual backend URL after Step 1)*

4. **Deploy Frontend**

## 🔧 Key Fixes Applied

### 1. Removed Root vercel.json ✅
**Before**: 
```json
{
  "installCommand": "cd frontend && npm install && cd ../backend && pip install -r requirements.txt"
}
```
**After**: File deleted - separate deployments

### 2. Fixed Frontend index.html ✅
**Before**: 
```html
<script type="module" src="/src/main.tsx"></script>
```
**After**: 
```html
<script type="module" src="./src/main.tsx"></script>
```

### 3. Backend Database Connection ✅
- Fixed localhost fallback issue
- Added proper Neon PostgreSQL configuration
- Enhanced error handling in tenant middleware
- Added health check endpoints

## 📁 Current Project Structure
```
HRMS-FINAL/
├── backend/
│   ├── vercel.json              # ✅ Backend-specific config
│   ├── vercel_wsgi.py           # ✅ WSGI entry point
│   ├── requirements.vercel.txt  # ✅ Optimized dependencies
│   ├── dashboard/settings.py    # ✅ Database config fixed
│   └── health_check.py          # ✅ Debugging endpoints
├── frontend/
│   ├── package.json             # ✅ Standard Vite config
│   ├── index.html               # ✅ Import path fixed
│   ├── vite.config.ts           # ✅ Build configuration
│   └── src/main.tsx             # ✅ Entry point
└── (root vercel.json REMOVED)   # ✅ No monorepo config
```

## 🧪 Testing After Deployment

### Backend Health Checks
- `https://your-backend.vercel.app/` → API info
- `https://your-backend.vercel.app/health/` → Basic health
- `https://your-backend.vercel.app/health/db/` → Database connection
- `https://your-backend.vercel.app/admin/` → Django admin

### Frontend
- `https://your-frontend.vercel.app/` → React application

## 🎯 Expected Results
1. **Backend Build**: ✅ Python 3.11 serverless function
2. **Frontend Build**: ✅ Static Vite build with React
3. **Database**: ✅ Neon PostgreSQL connection
4. **API Communication**: ✅ CORS-enabled frontend ↔ backend

## 🔍 Troubleshooting
- **Build Errors**: Check Vercel function logs
- **Database Issues**: Visit `/health/db/` endpoint
- **Frontend Errors**: Check browser console for API calls
- **CORS Issues**: Verify backend CORS settings include frontend URL

---

## 🎉 Status: READY FOR DEPLOYMENT
All critical issues have been resolved. Follow the steps above to deploy successfully.