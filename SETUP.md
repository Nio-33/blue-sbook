# 🔵 Blue's Book - Setup Guide

This guide will help you set up Blue's Book on your local machine for development.

## 📋 Prerequisites

Before you begin, make sure you have the following installed:

- **Python 3.9+** - [Download here](https://www.python.org/downloads/)
- **Node.js 16+** - [Download here](https://nodejs.org/) (for Tailwind CSS)
- **Git** - [Download here](https://git-scm.com/)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd blues-book
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
```

### 3. Configure Environment Variables

```bash
# Copy the example environment file
cp env.example .env

# Edit .env with your actual values
# You'll need to get API keys from the services below
```

### 4. Set Up Firebase

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or use an existing one
3. Enable Firestore Database and Firebase Storage
4. Go to Project Settings > Service Accounts
5. Generate a new private key and download the JSON file
6. Copy the values to your `.env` file

### 5. Set Up API-Football

1. Go to [API-Football](https://api-football.com/)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Add the key to your `.env` file

### 6. Install Frontend Dependencies (Optional)

```bash
# Install Tailwind CSS CLI (if you want to customize styles)
npm install -g tailwindcss

# Build custom CSS (optional)
cd frontend
tailwindcss -i css/tailwind.css -o css/tailwind.css --watch
```

### 7. Run the Application

```bash
# Make sure you're in the project root directory
python run.py
```

The application will be available at:
- **Frontend**: http://localhost:5000
- **API**: http://localhost:5000/api/v1
- **Health Check**: http://localhost:5000/health

## 🔧 Configuration Details

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Flask Configuration
FLASK_APP=backend/app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# API-Football Configuration
API_FOOTBALL_KEY=your-api-football-key-here
API_FOOTBALL_URL=https://api-football-v1.p.rapidapi.com/v3

# Firebase Configuration
FIREBASE_PROJECT_ID=your-firebase-project-id
FIREBASE_PRIVATE_KEY_ID=your-private-key-id
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nYour private key here\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=your-service-account@your-project.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=your-client-id
FIREBASE_AUTH_URI=https://accounts.google.com/o/oauth2/auth
FIREBASE_TOKEN_URI=https://accounts.google.com/o/oauth2/token

# Redis Configuration (Optional)
REDIS_URL=redis://localhost:6379
```

### Firebase Setup

1. **Create Firebase Project**:
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Click "Create a project"
   - Follow the setup wizard

2. **Enable Services**:
   - Go to "Firestore Database" and click "Create database"
   - Choose "Start in test mode" for development
   - Go to "Storage" and click "Get started"
   - Choose "Start in test mode"

3. **Get Service Account Key**:
   - Go to Project Settings > Service Accounts
   - Click "Generate new private key"
   - Download the JSON file
   - Copy the values to your `.env` file

### API-Football Setup

1. **Sign Up**: Go to [API-Football](https://api-football.com/) and create an account
2. **Get API Key**: Go to your dashboard and copy your API key
3. **Add to .env**: Paste the key into your `.env` file

## 📊 Data Synchronization

### Initial Data Sync

```bash
# Test API connections
python scripts/sync_squad.py --test-all

# Sync data from API-Football to Firebase
python scripts/sync_squad.py
```

### Scheduled Sync (Optional)

For production, you can set up a cron job to sync data daily:

```bash
# Add to crontab (runs daily at 2 AM)
0 2 * * * cd /path/to/blues-book && python scripts/sync_squad.py
```

## 🧪 Testing

### Backend Tests

```bash
cd backend
python -m pytest tests/ -v
```

### Manual Testing

1. **Health Check**: Visit http://localhost:5000/health
2. **API Endpoints**: Test the API endpoints using curl or Postman
3. **Frontend**: Open http://localhost:5000 in your browser

## 🚨 Troubleshooting

### Common Issues

1. **Firebase Connection Error**:
   - Check your Firebase credentials in `.env`
   - Ensure Firestore is enabled in your Firebase project
   - Verify the service account has proper permissions

2. **API-Football Error**:
   - Verify your API key is correct
   - Check if you've exceeded rate limits
   - Ensure you have an active subscription

3. **Python Import Errors**:
   - Make sure you're in the correct virtual environment
   - Install all requirements: `pip install -r backend/requirements.txt`
   - Check your Python path

4. **Frontend Not Loading**:
   - Ensure the Flask server is running
   - Check browser console for JavaScript errors
   - Verify the frontend files are in the correct location

### Debug Mode

Enable debug mode for more detailed error messages:

```bash
export FLASK_DEBUG=1
python run.py
```

## 📁 Project Structure

```
blues-book/
├── backend/                 # Flask backend
│   ├── app.py              # Main Flask application
│   ├── config.py           # Configuration settings
│   ├── requirements.txt    # Python dependencies
│   ├── services/           # Business logic services
│   ├── routes/             # API route handlers
│   └── utils/              # Utility functions
├── frontend/               # Frontend files
│   ├── index.html          # Main HTML page
│   ├── css/                # CSS styles
│   └── js/                 # JavaScript files
├── scripts/                # Utility scripts
│   └── sync_squad.py       # Data synchronization
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
├── run.py                  # Application runner
└── README.md               # Project documentation
```

## 🔄 Development Workflow

1. **Make Changes**: Edit the code in your preferred editor
2. **Test Locally**: Run `python run.py` to test changes
3. **Sync Data**: Use `python scripts/sync_squad.py` to update data
4. **Commit Changes**: Use git to commit your changes

## 📞 Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Review the logs for error messages
3. Ensure all prerequisites are installed
4. Verify your configuration files

## 🎉 Next Steps

Once you have Blue's Book running locally:

1. **Customize the UI**: Modify the frontend files to match your preferences
2. **Add Features**: Implement additional functionality as needed
3. **Deploy**: Follow the deployment guide to put it online
4. **Contribute**: Submit pull requests with improvements

---

**Made with 💙 for Chelsea FC fans worldwide**

*Keep The Blue Flag Flying High! KTBFFH*

