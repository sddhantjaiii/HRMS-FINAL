# Frontend Build Fix for Vercel Deployment

## Issue Description
The Vercel frontend build was failing with the error:
```
[vite]: Rollup failed to resolve import "/src/main.tsx" from "/vercel/path0/frontend/index.html".
This is most likely unintended because it can break your application at runtime.
```

## Root Cause
The `index.html` file was using an absolute path `/src/main.tsx` for the script import instead of a relative path. This works in development but fails during production builds with Vite/Rollup.

## Fix Applied
Changed the script import in `frontend/index.html` from:
```html
<script type="module" src="/src/main.tsx"></script>
```

To:
```html
<script type="module" src="./src/main.tsx"></script>
```

## Why This Fixes the Issue
- **Development**: Vite's dev server can resolve both absolute (`/src/main.tsx`) and relative (`./src/main.tsx`) paths
- **Production Build**: Rollup (used by Vite for building) expects relative paths from the HTML file to properly bundle the modules
- **Vercel**: Uses the production build process, so it requires the relative path format

## Expected Result
After this change, the Vercel build should succeed:
1. Vite will correctly resolve the `./src/main.tsx` import
2. The React application will build successfully
3. The static files will be deployed to Vercel

## Files Modified
- `frontend/index.html` - Changed script src from absolute to relative path

## Verification
The fix changes only the import path format without affecting any application logic. This is a standard practice for Vite/React applications deployed to production environments.