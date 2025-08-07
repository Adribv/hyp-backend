# Backend Deployment Guide for Render

This guide will walk you through deploying the SensAI backend to Render.

## Prerequisites

1. **Render Account**: Sign up at [render.com](https://render.com)
2. **GitHub Repository**: Your code should be in a GitHub repository
3. **Environment Variables**: Prepare your environment variables

## Step 1: Prepare Your Repository

### 1.1 Ensure Required Files Are Present

Make sure these files are in your `sensai-ai/` directory:
- `render.yaml` - Render configuration
- `build.sh` - Build script
- `gunicorn.conf.py` - Gunicorn configuration
- `requirements.txt` - Python dependencies
- `src/` - Your application code

### 1.2 Commit and Push Your Changes

```bash
git add .
git commit -m "feat: add Render deployment configuration"
git push origin main
```

## Step 2: Deploy to Render

### 2.1 Create a New Web Service

1. Go to your Render dashboard
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Select the repository containing your code

### 2.2 Configure the Service

**Basic Settings:**
- **Name**: `sensai-backend`
- **Environment**: `Docker`
- **Region**: Choose closest to your users
- **Branch**: `main` (or your default branch)
- **Root Directory**: `sensai-ai` (since your backend is in this subdirectory)
- **Dockerfile Path**: `./Dockerfile`

**Note**: Render will automatically use the Dockerfile for building and running your application.

### 2.3 Set Environment Variables

In the Render dashboard, go to "Environment" tab and add these variables:

**Required Variables:**
```
OPENAI_API_KEY=your_openai_api_key
GOOGLE_CLIENT_ID=your_google_client_id
ENV=production
RENDER=true
ALLOWED_ORIGINS=https://your-frontend-domain.com,https://www.your-frontend-domain.com
```

**Optional Variables (set as needed):**
```
S3_BUCKET_NAME=your_s3_bucket_name
S3_FOLDER_NAME=your_s3_folder_name
BUGSNAG_API_KEY=your_bugsnag_key
SLACK_USER_SIGNUP_WEBHOOK_URL=your_slack_webhook
SLACK_COURSE_CREATED_WEBHOOK_URL=your_slack_webhook
SLACK_USAGE_STATS_WEBHOOK_URL=your_slack_webhook
PHOENIX_ENDPOINT=your_phoenix_endpoint
PHOENIX_API_KEY=your_phoenix_key
```

### 2.4 Deploy

Click "Create Web Service" to start the deployment.

## Step 3: Verify Deployment

### 3.1 Check Build Logs

Monitor the build process in the Render dashboard. Common issues:
- Missing dependencies in `requirements.txt`
- Environment variable issues
- File permission problems

### 3.2 Test the API

Once deployed, test your endpoints:

```bash
# Health check
curl https://your-app-name.onrender.com/health

# Test other endpoints
curl https://your-app-name.onrender.com/docs

# Or use the test script
python test_deployment.py https://your-app-name.onrender.com
```

### 3.3 Check Logs

In Render dashboard, go to "Logs" tab to monitor:
- Application logs
- Error messages
- Performance metrics

## Step 4: Configure Custom Domain (Optional)

1. Go to "Settings" tab in your Render service
2. Click "Add Custom Domain"
3. Follow the DNS configuration instructions

## Step 5: Update Frontend Configuration

Once your backend is deployed, update your frontend to use the new backend URL:

```typescript
// In your frontend environment variables
NEXT_PUBLIC_BACKEND_URL=https://your-app-name.onrender.com
```

## Troubleshooting

### Common Issues

1. **Build Failures**
   - Check `requirements.txt` for missing dependencies
   - Verify Python version compatibility
   - Check build logs for specific errors

2. **Runtime Errors**
   - Verify all environment variables are set
   - Check application logs for error details
   - Ensure database initialization is working

3. **Application Exited Early**
   - This usually means the app crashed during startup
   - Check if all required environment variables are set
   - Try the simplified deployment approach (see below)
   - Run the minimal test locally: `python test_minimal.py`

4. **Performance Issues**
   - Monitor resource usage in Render dashboard
   - Consider upgrading to a higher plan if needed
   - Optimize database queries and file operations

5. **CORS Issues**
   - Update CORS settings in `main.py` to allow your frontend domain
   - Test with browser developer tools

### If Deployment Still Fails

Try these approaches:

1. **Use the simplified Dockerfile**:
   ```bash
   # Rename the simplified Dockerfile
   mv Dockerfile.simple Dockerfile
   ```

2. **Test Docker build locally**:
   ```bash
   cd sensai-ai
   docker build -t sensai-backend .
   docker run -p 8000:8000 -e OPENAI_API_KEY=test -e GOOGLE_CLIENT_ID=test sensai-backend
   ```

3. **Check Docker logs**:
   - In Render dashboard, go to "Logs" tab
   - Look for Docker build errors or runtime errors
   - Common issues: missing dependencies, permission errors, port conflicts

4. **Test locally first**:
   ```bash
   cd sensai-ai
   python test_minimal.py
   cd src
   python startup.py
   uvicorn api.main:app --reload
   ```

### Useful Commands

```bash
# Check local build
cd sensai-ai
python -m pip install -r requirements.txt
cd src
python startup.py
uvicorn api.main:app --reload

# Test with curl
curl -X GET "http://localhost:8000/health"
```

## Monitoring and Maintenance

### 1. Set Up Monitoring
- Configure health checks
- Set up error tracking (Bugsnag)
- Monitor performance metrics

### 2. Regular Maintenance
- Keep dependencies updated
- Monitor logs for issues
- Backup database regularly

### 3. Scaling Considerations
- Render starter plan has limitations
- Consider upgrading for higher traffic
- Implement caching strategies

## Next Steps

After successful backend deployment:
1. Deploy frontend to Vercel/Netlify
2. Configure domain and SSL
3. Set up monitoring and alerts
4. Test end-to-end functionality

## Support

If you encounter issues:
1. Check Render documentation
2. Review application logs
3. Test locally first
4. Contact Render support if needed
