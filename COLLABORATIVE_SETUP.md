# Collaborative Live Report Setup Guide

## Overview
The live report now supports **real-time collaborative editing**. When any user updates and saves a field, the changes are automatically synced and visible to all other users viewing the report.

## Features
✅ **Real-time Sync**: Changes are saved to a central server and synced to all users  
✅ **Auto-save**: Automatically saves changes 2 seconds after you stop typing  
✅ **Live Updates**: Polls for updates every 5 seconds  
✅ **Offline Fallback**: Works locally if server is unavailable  
✅ **User Tracking**: Tracks who made the last update  
✅ **Visual Feedback**: Shows sync status with a live indicator  

## Setup Instructions

### 1. Start the Backend Server

The collaborative feature requires the Flask API server to be running.

**Option A: Local Development**
```bash
# Install dependencies (if not already installed)
pip install flask flask-cors psycopg2

# Start the server
python api_server.py
```

The server will start at `http://localhost:5000`

**Option B: Deploy to Production**

For GitHub Pages or public deployment, you need to deploy the API server separately:

1. **Deploy to Railway/Render/Heroku**:
   - Upload `api_server.py` and `requirements.txt`
   - Set environment variables if needed
   - Get your production API URL

2. **Update the API URL in live_report.html**:
   ```javascript
   const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
       ? 'http://localhost:5000/api' 
       : 'https://your-api-server.com/api'; // ← Update this with your deployed API URL
   ```

### 2. Open the Live Report

Simply open `live_report.html` in your browser:
- Locally: `file:///path/to/live_report.html`
- GitHub Pages: `https://vishnuramalingam07.github.io/Myisp_Tools/live_report.html`

### 3. Using the Collaborative Features

1. **First Time**: You'll be prompted to enter your name for tracking
2. **Making Changes**: 
   - Edit any input field or dropdown
   - Changes auto-save after 2 seconds
   - Click the "Save" button for immediate save
3. **Seeing Updates**: 
   - Other users' changes appear automatically every 5 seconds
   - A notification shows when new updates are available
4. **Sync Status**: 
   - 🟢 Green indicator = Live sync active
   - ⚫ Gray indicator = Offline mode (local only)

## How It Works

### Architecture
```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   User 1    │      │   API       │      │   User 2    │
│   Browser   │◄────►│   Server    │◄────►│   Browser   │
└─────────────┘      └─────────────┘      └─────────────┘
                             │
                             ▼
                     ┌─────────────┐
                     │shared_report│
                     │_data.json   │
                     └─────────────┘
```

1. **User makes a change** → Auto-saves locally after 2s
2. **Data sent to API** → Saved to `shared_report_data.json`
3. **Other users polling** → Fetch updates every 5s
4. **Updates applied** → Silently update inactive tabs

### Data Storage
- **File**: `shared_report_data.json` (created automatically)
- **Format**: JSON with tab IDs as keys
- **Includes**: Field values, timestamps, and user tracking

### API Endpoints
- `POST /api/shared-data/<tab_id>` - Save tab data
- `GET /api/shared-data/<tab_id>` - Get tab data
- `GET /api/shared-data` - Get all tab data
- `GET /api/health` - Check server status

## Troubleshooting

### Issue: "Offline Mode" showing
**Solution**: 
- Ensure the API server is running (`python api_server.py`)
- Check the API_BASE_URL in live_report.html matches your server URL
- Verify no firewall/CORS issues blocking requests

### Issue: Changes not syncing
**Solution**:
- Open browser console (F12) to check for errors
- Verify `shared_report_data.json` file is being created/updated
- Ensure the server has write permissions in the directory

### Issue: Getting CORS errors
**Solution**:
- The server already has CORS enabled via `flask-cors`
- If deploying, ensure CORS is configured in your hosting platform

## Deployment Checklist

For production deployment on GitHub Pages:

- [ ] Deploy API server to Railway/Render/Heroku
- [ ] Update `API_BASE_URL` in live_report.html with production URL
- [ ] Test connectivity from GitHub Pages to API
- [ ] Configure CORS if needed
- [ ] Set up SSL/HTTPS for secure connections
- [ ] (Optional) Add authentication for security

## Security Notes

⚠️ **Current Implementation**: Basic collaborative editing without authentication

For production use, consider adding:
- User authentication (OAuth, JWT)
- Role-based access control
- Data validation on the server
- Rate limiting
- Backup/versioning of shared data

## Support

For issues or questions:
- Check browser console for error messages
- Verify server logs for API errors
- Test with curl: `curl http://localhost:5000/api/health`

---

**Version**: 1.0  
**Last Updated**: April 17, 2026
