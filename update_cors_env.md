# CORS Fix for Render Deployment

## Immediate Fix

You need to update the environment variables in your Render dashboard:

### Go to Render Dashboard:
1. Navigate to your `hyp-backend-2` service
2. Go to "Environment" tab
3. Add/Update this environment variable:

```
ALLOWED_ORIGINS=http://localhost:3000,https://hyp-frontend.onrender.com
```

### For Development (temporary):
```
ALLOWED_ORIGINS=*
```

### For Production (recommended):
```
ALLOWED_ORIGINS=http://localhost:3000,https://hyp-frontend.onrender.com
```

## Alternative: Quick Fix

If you want to allow all origins temporarily for testing:

1. In Render dashboard, set:
   ```
   ALLOWED_ORIGINS=*
   ENV=development
   ```

2. Redeploy your service

## Test the Fix

After updating the environment variables and redeploying:

```bash
# Test CORS headers
curl -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: GET" \
     -H "Access-Control-Request-Headers: X-Requested-With" \
     -X OPTIONS \
     https://hyp-backend-2.onrender.com/health
```

You should see `Access-Control-Allow-Origin: http://localhost:3000` in the response headers.

## Next Steps

1. Update environment variables in Render
2. Redeploy the service
3. Test your frontend again
4. Once working, update to production CORS settings
