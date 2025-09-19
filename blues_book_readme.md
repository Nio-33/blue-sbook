# 🔵 Blue's Book

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-lightgrey.svg)](https://flask.palletsprojects.com/)
[![Firebase](https://img.shields.io/badge/Firebase-Firestore-orange.svg)](https://firebase.google.com/)

> **The definitive digital reference for Chelsea FC squad information**

Blue's Book is a modern, interactive web application that provides Chelsea FC fans with comprehensive, real-time information about current squad players and management. Built with Flask, Firebase, and powered by live football APIs.

## 🌟 Features

### MVP (Phase 1)
- 🔍 **Fast Autocomplete Search** - Find players instantly with partial name matching
- 👤 **Detailed Player Profiles** - Age, position, signing fee, fun facts, and photos
- 🎲 **Random Player Discovery** - Daily featured player for squad exploration
- 📱 **Mobile-First Design** - Responsive UI optimized for all devices
- ⚡ **Real-Time Data** - Always up-to-date via API-Football integration
- 🔧 **Smart Filtering** - Sort by position, signing fee, age, jersey number

### Coming Soon (Phase 2)
- 📊 **Transfer Analytics** - Visualize spending patterns with Chart.js
- 📄 **Export Features** - Share player cards as PNG/PDF
- 🔗 **Public API** - RESTful endpoints for developers
- 📈 **Squad Insights** - Historical timelines and statistics

### Future (Phase 3)
- 🎥 **Match Highlights** - Embedded video content for players
- ⭐ **Iconic Moments** - Curated memorable plays and achievements
- 👥 **User Accounts** - Personalized favorites and preferences

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Node.js (for Tailwind CSS)
- Firebase account
- API-Football account

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/blues-book.git
   cd blues-book
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and Firebase credentials
   ```

4. **Initialize Firebase**
   ```bash
   # Install Firebase CLI
   npm install -g firebase-tools
   firebase login
   firebase init
   ```

5. **Install frontend dependencies**
   ```bash
   cd frontend
   npm install
   npm run build
   cd ..
   ```

6. **Run the application**
   ```bash
   flask run
   ```

Visit `http://localhost:5000` to see Blue's Book in action!

## 🏗️ Project Structure

```
blues-book/
│
├── backend/
│   ├── app.py                     # Flask application entry point
│   ├── config.py                  # Configuration settings
│   ├── requirements.txt           # Python dependencies
│   │
│   ├── services/
│   │   ├── firebase_service.py    # Firebase/Firestore operations
│   │   └── data_loader.py         # API data sync and seeding
│   │
│   ├── routes/
│   │   ├── player_routes.py       # Player API endpoints
│   │   ├── manager_routes.py      # Manager API endpoints
│   │   └── search_routes.py       # Search and autocomplete
│   │
│   └── utils/
│       ├── validators.py          # Input validation
│       ├── formatters.py          # Data formatting utilities
│       └── randomizer.py          # Random player logic
│
├── frontend/
│   ├── index.html                 # Main application page
│   ├── css/
│   │   └── tailwind.css          # Tailwind CSS styles
│   └── js/
│       ├── app.js                # Main application logic
│       ├── search.js             # Search functionality
│       └── player.js             # Player profile rendering
│
├── scripts/
│   └── sync_squad.py             # Daily data synchronization
│
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore rules
└── README.md                      # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Flask Configuration
FLASK_APP=backend/app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key

# API-Football
API_FOOTBALL_KEY=your-api-football-key
API_FOOTBALL_URL=https://api-football-v1.p.rapidapi.com/v3

# Firebase Configuration
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_PRIVATE_KEY_ID=your-private-key-id
FIREBASE_PRIVATE_KEY=your-private-key
FIREBASE_CLIENT_EMAIL=your-client-email
FIREBASE_CLIENT_ID=your-client-id
FIREBASE_AUTH_URI=https://accounts.google.com/o/oauth2/auth
FIREBASE_TOKEN_URI=https://accounts.google.com/o/oauth2/token

# Redis (Optional - for caching)
REDIS_URL=redis://localhost:6379
```

### Firebase Setup

1. Create a new Firebase project at [Firebase Console](https://console.firebase.google.com/)
2. Enable Firestore Database and Firebase Storage
3. Generate service account credentials
4. Add credentials to your `.env` file

### API-Football Setup

1. Sign up at [API-Football](https://api-football.com/)
2. Subscribe to a plan (free tier available)
3. Get your API key from the dashboard
4. Add the key to your `.env` file

## 📊 API Endpoints

### Players
```
GET  /api/v1/players              # List all players with optional filtering
GET  /api/v1/players/<id>         # Get specific player details
GET  /api/v1/players/random       # Get random player of the day
GET  /api/v1/players/search       # Autocomplete search
```

### Managers
```
GET  /api/v1/managers/current     # Get current Chelsea manager
```

### Search
```
GET  /api/v1/search               # Search across players and managers
```

### Example Response
```json
{
  "name": "Cole Palmer",
  "birth_year": 2002,
  "age": 23,
  "jersey_number": 20,
  "position": "Forward",
  "signing_fee": "£42.5M",
  "weekly_salary": "£75,000",
  "years_at_club": "2023–Present",
  "image_url": "https://firebasestorage.googleapis.com/.../cole_palmer.jpg",
  "fun_facts": [
    "Scored his first Chelsea goal vs Luton Town on August 25, 2023",
    "Won UEFA Conference League in 2025"
  ]
}
```

## 🧪 Testing

```bash
# Run backend tests
cd backend
python -m pytest tests/ -v

# Run frontend tests (if available)
cd frontend
npm test

# Run integration tests
python -m pytest tests/integration/ -v
```

## 📈 Performance

- **Search Response Time**: < 300ms for cached queries
- **Page Load Time**: < 2 seconds on 3G connection
- **API Uptime**: 99.5% availability target
- **Mobile Performance**: Lighthouse score > 90

## 🚀 Deployment

### Development
```bash
flask run --debug
```

### Production

#### Using Docker
```bash
docker build -t blues-book .
docker run -p 5000:5000 --env-file .env blues-book
```

#### Using Railway/Render
1. Connect your GitHub repository
2. Set environment variables in dashboard
3. Deploy automatically on push to main branch

#### Using Heroku
```bash
heroku create blues-book
heroku config:set FLASK_APP=backend/app.py
heroku config:set --file .env
git push heroku main
```

## 🤝 Contributing

We welcome contributions from the Chelsea FC community! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Reporting Issues

Found a bug or have a feature request? Please [open an issue](https://github.com/yourusername/blues-book/issues) with:

- Clear description of the problem or suggestion
- Steps to reproduce (for bugs)
- Expected vs actual behavior
- Screenshots (if applicable)

## 📝 Data Sources

- **Primary**: [API-Football](https://api-football.com/) - Player statistics and squad information
- **Secondary**: [TheSportsDB](https://thesportsdb.com/) - Additional player images and metadata
- **Fallback**: Manual curation for missing or incorrect data

## 🔒 Privacy & Security

- **No Personal Data Collection**: Blue's Book doesn't collect or store user personal information
- **GDPR Compliant**: All data handling follows European privacy regulations
- **Secure API Keys**: All sensitive credentials are environment-variable protected
- **Rate Limited**: API endpoints include rate limiting to prevent abuse

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Chelsea FC](https://www.chelseafc.com/) - For being the inspiration behind this project
- [API-Football](https://api-football.com/) - For providing comprehensive football data
- [Firebase](https://firebase.google.com/) - For reliable backend services
- [Tailwind CSS](https://tailwindcss.com/) - For beautiful, responsive styling
- The Chelsea FC fan community - For feedback and support

## 💬 Community

- **Discord**: [Join our Discord](https://discord.gg/chelsea-blues-book)
- **Twitter**: [@BluesBookApp](https://twitter.com/BluesBookApp)
- **Reddit**: [r/BluesBook](https://reddit.com/r/BluesBook)

---

**Made with 💙 for Chelsea FC fans worldwide**

*Keep The Blue Flag Flying High! KTBFFH*

## 📞 Support

Having trouble? We're here to help:

- 📧 Email: support@bluesbook.app
- 💬 Discord: [Chelsea Blues Book Community](https://discord.gg/chelsea-blues-book)
- 🐛 Bug Reports: [GitHub Issues](https://github.com/yourusername/blues-book/issues)
- 📖 Documentation: [Wiki](https://github.com/yourusername/blues-book/wiki)

---

*Last updated: August 26, 2025*