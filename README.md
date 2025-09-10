# 🏏 Cricket Analytics Dashboard

A comprehensive cricket analytics dashboard with live scorecard, player management, and match tracking capabilities.

![Cricket Analytics Dashboard](https://img.shields.io/badge/Status-Active-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-2.3+-lightgrey)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

- 🏆 **Live Scorecard** - Real-time cricket match display
- 📊 **Player Analytics** - Comprehensive player statistics and management
- 🎯 **Match Management** - Complete CRUD operations for matches
- 🌐 **Live Cricket Data** - Integration with CricketData.org API
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile
- 🔄 **Auto-refresh** - Live data updates every 30 seconds
- 💾 **SQLite Database** - Local data storage with sample data

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/cricket-analytics-dashboard.git
   cd cricket-analytics-dashboard
   ```

2. **Set up virtual environment** (recommended)
   ```bash
   python -m venv cricket_env
   source cricket_env/bin/activate  # On Windows: cricket_env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Start the application**
   ```bash
   python app.py
   ```

5. **Access the dashboard**
   Open your browser and go to: `http://127.0.0.1:8000`

## 📁 Project Structure

```
cricket-analytics-dashboard/
├── backend/                 # Flask backend
│   ├── app.py              # Main Flask application
│   ├── requirements.txt    # Python dependencies
│   └── cricket_analytics.db # SQLite database (auto-generated)
├── frontend/               # Frontend files
│   └── dashboard.html      # Main dashboard interface
├── docs/                   # Documentation and GitHub Pages
├── .gitignore             # Git ignore rules
├── README.md              # Project documentation
└── LICENSE                # MIT License
```

## 🛠️ Technology Stack

### Backend
- **Flask** - Python web framework
- **SQLite** - Database for storing cricket data
- **Flask-CORS** - Cross-origin resource sharing
- **Requests** - HTTP library for API calls

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with gradients and animations
- **JavaScript** - Dynamic functionality and API integration
- **Responsive Design** - Mobile-first approach

### External APIs
- **CricketData.org** - Live cricket data integration

## 🎯 API Endpoints

### Player Management
- `GET /api/players` - Get all players
- `POST /api/players` - Add new player
- `PUT /api/players/{id}` - Update player
- `DELETE /api/players/{id}` - Delete player

### Match Management
- `GET /api/matches` - Get all matches
- `POST /api/matches` - Add new match
- `PUT /api/matches/{id}` - Update match
- `DELETE /api/matches/{id}` - Delete match

### Live Data
- `GET /api/dashboard/live` - Get live scorecard data
- `GET /api/dashboard/analytics` - Get player analytics
- `GET /api/live/current-matches` - Get current matches from API

### Utility
- `GET /health` - Health check endpoint
- `GET /api/test/cricket-api` - Test external API connection

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
CRICKET_API_KEY=your-cricket-data-api-key
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
PORT=8000
```

### Database

The SQLite database is automatically created with sample data on first run. No additional setup required.

## 🚀 Deployment

### Local Development
```bash
cd backend
python app.py
```

### Production Deployment

#### Using Docker
```bash
docker-compose up -d
```

#### Using Heroku
```bash
git push heroku main
```

#### Using Railway
1. Connect your GitHub repository to Railway
2. Deploy automatically

## 📱 Mobile Support

The dashboard is fully responsive and works great on:
- 📱 Mobile phones (iOS/Android)
- 📱 Tablets
- 💻 Desktop computers
- 🖥️ Large displays

## 🎮 Keyboard Shortcuts

- `Ctrl + 1` - Switch to Live Scorecard
- `Ctrl + 2` - Switch to Live Cricket Data
- `Ctrl + 3` - Switch to Player Management
- `Ctrl + 4` - Switch to Match Management
- `Esc` - Close forms/modals

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📊 Sample Data

The application comes with sample cricket data including:
- **Players**: Virat Kohli, Steve Smith, Joe Root, and more
- **Matches**: India vs Australia, England vs New Zealand
- **Statistics**: Runs, strike rates, bowling figures

## 🔍 Features in Detail

### Live Scorecard
- Real-time match scores
- Current batsmen statistics
- Over-by-over progression
- Match status tracking

### Player Analytics
- Top run scorers
- Best strike rates
- Team comparisons
- Player performance trends

### Match Management
- Add/edit/delete matches
- Score updates
- Venue information
- Match status (Live/Completed/Upcoming)

## 🛣️ Roadmap

- [ ] Real-time commentary
- [ ] Ball-by-ball tracking
- [ ] Advanced statistics (wagon wheels, manhattan graphs)
- [ ] User authentication
- [ ] Multiple tournament support
- [ ] Export data to Excel/PDF
- [ ] Push notifications for score updates

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)

## 🙏 Acknowledgments

- [CricketData.org](https://cricketdata.org) for providing cricket data API
- Flask community for the excellent framework
- All contributors who help improve this project

## 📞 Support

If you have any questions or need help with setup, please:
1. Check the [Issues](https://github.com/yourusername/cricket-analytics-dashboard/issues) page
2. Create a new issue if your problem isn't already listed
3. Provide detailed information about your environment and the issue

---

⭐ **Star this repository if you found it helpful!** ⭐