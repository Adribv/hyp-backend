@echo off
echo Creating backend environment file for SensAI...

echo Creating backend .env file...
(
echo # Google OAuth ^(your actual credentials^)
echo GOOGLE_CLIENT_ID=your-google-client-id-here
echo.
echo # OpenAI
echo OPENAI_API_KEY=your-openai-api-key
echo.
echo # Optional: S3 Configuration ^(for production^)
echo S3_BUCKET_NAME=your-s3-bucket
echo S3_FOLDER_NAME=your-s3-folder
echo.
echo # Optional: Error Tracking
echo BUGSNAG_API_KEY=your-bugsnag-key
echo ENV=development
echo.
echo # Optional: Slack Webhooks
echo SLACK_USER_SIGNUP_WEBHOOK_URL=your-slack-webhook
echo SLACK_COURSE_CREATED_WEBHOOK_URL=your-slack-webhook
echo SLACK_USAGE_STATS_WEBHOOK_URL=your-slack-webhook
) > .env

echo Backend .env file created successfully!
echo.
echo IMPORTANT: You still need to:
echo 1. Add your OpenAI API key to the .env file
echo 2. Add redirect URIs to Google Cloud Console:
echo    - http://localhost:3000/api/auth/callback/google
echo.
pause 