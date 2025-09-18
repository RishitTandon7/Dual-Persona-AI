# 🚀 Deploying AI Shopping Assistant on Render

This guide will help you deploy the AI Shopping Assistant to Render's cloud platform.

## Prerequisites

- A Render account (free tier available)
- Git repository with your code (GitHub, GitLab, or Bitbucket)

## Deployment Steps

### 1. Prepare Your Repository

Make sure your repository contains the following files:
- `app.py` - Main Flask application
- `requirements.txt` - Python dependencies (including gunicorn)
- `render.yaml` - Render configuration
- `start.sh` - Startup script

### 2. Connect to Render

1. Go to [render.com](https://render.com) and sign up/login
2. Click "New +" and select "Web Service"
3. Connect your Git repository (GitHub, GitLab, or Bitbucket)
4. Render will automatically detect the `render.yaml` file

### 3. Configuration

The `render.yaml` file contains:
```yaml
services:
  - type: web
    name: ai-shopping-assistant
    env: python
    plan: free
    buildCommand: "pip install -r requirements.txt"
    startCommand: "./start.sh"
    autoDeploy: true
```

### 4. Environment Variables (Optional)

You can set environment variables in the Render dashboard:
- `FLASK_ENV=production`
- `PORT=5000` (automatically set by Render)
- `CACHE_TIMEOUT=300`
- `MAX_RESULTS=12`

### 5. Deploy

Render will automatically:
1. Install dependencies from `requirements.txt`
2. Build your application
3. Start the service using the `start.sh` script
4. Provide a public URL for your application

## File Structure for Render

```
.
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── render.yaml         # Render configuration
├── start.sh           # Startup script
├── enhanced-index.html # Frontend HTML
├── modern-styles.css   # CSS styles
├── script.js          # Frontend JavaScript
└── (other supporting files)
```

## Troubleshooting

### Common Issues

1. **Build Fails**: Check that all dependencies are in `requirements.txt`
2. **Application Won't Start**: Verify `start.sh` has execute permissions
3. **Port Issues**: Render automatically sets the `$PORT` environment variable

### Logs

Check the logs in the Render dashboard for:
- Build logs (during deployment)
- Runtime logs (after deployment)

## Free Tier Limitations

- 750 hours/month of free usage
- Automatic shutdown after 15 minutes of inactivity
- Limited to 1 web service on free tier

## Performance Tips

- Use 2 workers for optimal performance on free tier
- Implement proper caching strategies
- Monitor memory usage in the Render dashboard

## Support

For Render-specific issues, refer to:
- [Render Documentation](https://render.com/docs)
- [Python on Render Guide](https://render.com/docs/deploy-python)

Your application will be available at: `https://your-app-name.onrender.com`
