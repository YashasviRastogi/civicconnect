# CivicConnect README.md

CivicConnect connects citizens with local government for efficient issue reporting. This README includes the actual file organization from the repository.

## Project Overview
CivicConnect enables residents to report civic issues like potholes and waste management with GPS and photos. Government officials track and resolve reports via an admin dashboard for faster civic services.

## File Structure
```
civicconnect/
├── README.md                 # Project documentation
├── client/                   # React frontend
│   ├── public/
│   │   ├── index.html
│   │   └── favicon.ico
│   ├── src/
│   │   ├── components/
│   │   │   ├── ReportForm.jsx
│   │   │   ├── IssueCard.jsx
│   │   │   └── MapView.jsx
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   └── Admin.jsx
│   │   ├── App.js
│   │   ├── index.js
│   │   └── styles.css
│   └── package.json
├── server/                   # Node.js/Express backend
│   ├── models/
│   │   ├── Issue.js         # Mongoose schema for reports
│   │   └── User.js
│   ├── routes/
│   │   ├── issues.js        # API endpoints for reports
│   │   └── auth.js
│   ├── middleware/
│   │   └── auth.js
│   ├── server.js
│   └── package.json
├── docs/
│   └── API.md               # API documentation
├── .env.example             # Environment variables template
├── .gitignore
└── package.json             # Root dependencies (if monorepo)
```

## Features
- Photo uploads with GPS location pinning.
- Real-time issue status updates.
- Admin dashboard with task assignment.
- Email/SMS notifications.
- Responsive mobile-first design.

## Tech Stack
- **Frontend**: React.js + Tailwind CSS
- **Backend**: Node.js + Express.js
- **Database**: MongoDB
- **Maps**: Google Maps API
- **Auth**: Firebase/JWT

## Quick Start
1. Clone: `git clone https://github.com/YashasviRastogi/civicconnect.git`
2. Backend: `cd server && npm install && npm start`
3. Frontend: `cd client && npm install && npm run dev`
4. Copy `.env.example` to `.env` and add API keys
5. Access: `http://localhost:3000`

## Setup Environment
Create `.env` files in both `client/` and `server/`:

**server/.env:**
```
MONGODB_URI=your_mongo_connection
GOOGLE_MAPS_API_KEY=your_key
JWT_SECRET=your_secret
PORT=5000
```

**client/.env:**
```
REACT_APP_MAPS_API_KEY=your_key
REACT_APP_API_URL=http://localhost:5000/api
```

## Contributing
1. Fork → Clone → Create feature branch
2. Update files in appropriate directories (`client/src/components/`, `server/routes/`)
3. Test locally, then PR
4. Focus areas: mobile UX, sustainability metrics, admin analytics

## Deployment
- Frontend: Vercel/Netlify
- Backend: Render/Heroku
- Database: MongoDB Atlas
- http://localhost:5000

MIT License. Open issues for hackathon collabs or bugs.
