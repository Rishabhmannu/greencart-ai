# GreenCart 🌱 - AI-Powered Sustainable Shopping Platform

## 🎯 Features in Action

### 🧮 EarthScore Calculator
![EarthScore Calculator](./images/calculator.jpeg)

### 🤖 AI Chatbot Assistant
![Chatbot Demo1](./images/chatbot1.jpeg)
![Chatbot Demo2](./images/chatbot2.png)
![Chatbot Demo3](./images/chatbot3.png)
![Chatbot Demo4](./images/chatbot4.png)
![Chatbot Demo5](./images/chatbot5.png) **Dynamic Filtering based on User Queries using Advanced NLP!**
![Chatbot Demo6](./images/chatbot6.png) **Express Checkout Option directly from within the Chatbot itself!**

### 📊 User Impact Dashboard
![Impact Dashboard](./images/dashboard.jpeg)

### 🛒 GreenCart Landing Page
![GreenCart Landing](./images/landing-greencart.jpeg)

### 📦 Order Flow
![Order Step 1](./images/order1.jpeg)
![Order Step 2](./images/order2.jpeg)

### 🧾 Product Parameters Analysis
![Product Parameters](./images/product-params.jpeg)

### 👥 Smart Group Buying
![Group Buying](./images/group-buying.jpeg)

Transform your shopping habits with AI-powered sustainability scoring, group buying, and real-time carbon tracking.

GreenCart is an innovative e-commerce platform that gamifies sustainable shopping through EarthScore ratings (0-100), AI-driven group buying recommendations using DBSCAN clustering, and a multi-agent chatbot powered by Google Gemini 1.5 Pro or OpenAI's GPT-4 models. It promotes eco-conscious consumer behavior through real-time carbon tracking, achievement systems, and community-driven bulk purchasing.

## 🌟 Key Features

### 🎯 EarthScore Intelligence
- **Comprehensive Sustainability Rating**: Every product rated 0-100 based on:
  - Carbon footprint (30%)
  - Materials & packaging (25%)
  - Ethical sourcing (25%)
  - Product longevity (20%)
- **Real-time Impact Calculation**: See CO2 savings for every purchase
- **Smart Recommendations**: AI suggests greener alternatives

### 🤖 Multi-Agent AI Assistant
- **Intelligent Routing**: Orchestrator agent delegates to specialized agents
- **Shopping Assistant**: Natural language product search and recommendations
- **Sustainability Advisor**: Environmental impact education and tips
- **Deal Finder**: Group buying opportunities and savings calculations
- **Checkout Assistant**: Cart optimization and packaging suggestions

### 👥 Smart Group Buying
- **DBSCAN Clustering Algorithm**: Automatically groups nearby users
- **Dynamic Savings**: 15-30% cost reduction, 60% less packaging
- **Location-Based Matching**: Find neighbors with similar shopping needs
- **Real-time Progress Tracking**: Visual indicators for group completion

### 🎮 Gamification System
- **User Levels**: Progress through sustainability milestones
- **Achievements**: 
  - "Carbon Warrior" - Save 10kg CO2
  - "Group Buy Champion" - Lead 5 successful groups
  - "Eco Hero" - Maintain 80+ average EarthScore
- **Leaderboard**: Community impact rankings
- **Rewards**: Unlock badges and exclusive discounts

### 📊 Advanced Analytics
- **Personal Dashboard**: Track your environmental impact over time
- **Carbon Footprint Visualization**: See your CO2 savings in real terms
- **Product Parameter Database**: Access detailed sustainability metrics
- **Impact Calculator**: Estimate environmental effects before purchase

## 🚀 Live Demo

🌐 **Frontend**: [Your deployment URL]  
🔧 **Backend API**: [Your API docs URL]

## Login Info

- Users can register with any email and password, an email with confirmation code will be sent via SendGrid Email API by Twilio.
- Demo account credentials:
  - **Username**: iit2022131@iiita.ac.in
  - **Password**: password

## 🛠️ Technology Stack

### Frontend
- **Framework**: React 18 with TypeScript
- **UI Library**: Material-UI v5
- **State Management**: React Context API
- **Authentication**: Firebase Auth
- **Build Tool**: Create React App
- **Styling**: CSS Modules + Material-UI theming

### Backend
- **Framework**: FastAPI (Python 3.10+)
- **AI/ML**: 
  - LangGraph for multi-agent orchestration
  - Google Gemini 1.5 Pro / OpenAI GPT-4 for NLP
  - scikit-learn for clustering and predictions
- **Database**: 
  - Redis for cart persistence
  - CSV files for product data (PostgreSQL ready)
- **API**: RESTful architecture

### DevOps
- **Deployment**: Cloud hosting (AWS EC2/Heroku/Vercel)
- **Process Manager**: systemd / PM2
- **Version Control**: Git/GitHub
- **CI/CD**: GitHub Actions

## 📁 Project Architecture

```
greencart/
├── backend/
│   ├── agents/               # Multi-agent system
│   │   ├── orchestrator.py   # Request routing
│   │   ├── shopping_assistant.py
│   │   ├── sustainability_advisor.py
│   │   ├── deal_finder.py
│   │   └── checkout_assistant.py
│   ├── services/             # Business logic
│   │   ├── cart_service.py   # Redis cart management
│   │   ├── group_buy_service.py
│   │   └── clustering_service.py  # DBSCAN implementation
│   ├── ml/                   # Machine learning
│   │   ├── engine.py         # EarthScore calculation
│   │   └── model.pkl         # Trained model
│   └── main.py              # FastAPI application
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── Chatbot.tsx   # AI assistant interface
│   │   │   ├── Dashboard.tsx # Gamification dashboard
│   │   │   ├── Cart.tsx      # Shopping cart
│   │   │   └── checkout/     # Checkout flow
│   │   ├── context/          # Global state
│   │   └── services/         # API integration
│   └── public/
│       └── images/           # Category images
└── data/
    ├── products_large.csv    # 200+ products database
    └── users_pincodes.csv    # User location data
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.10+
- Node.js 16+
- Redis Server
- Git

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/Rishabhmannu/greencart-ai.git
cd greencart-ai/backend
```

2. Create virtual environment:
```bash
python -m venv greencart_env
source greencart_env/bin/activate  # On Windows: greencart_env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set environment variables:
```bash
export GOOGLE_API_KEY="your-gemini-api-key"
export OPENAI_API_KEY="your-openai-api-key"
export PYTHONPATH="${PWD}:$PYTHONPATH"
```

Alternatively, create a `.env` file in the `/backend` directory:
```env
GOOGLE_API_KEY=your-gemini-api-key
OPENAI_API_KEY=your-openai-api-key
```

5. Start the backend:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd ../frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env` file:
```env
REACT_APP_API_URL=http://localhost:8000
PORT=3111
```

4. Start development server:
```bash
npm start
```

## 📡 API Documentation

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/products` | GET | List all products with EarthScores |
| `/api/products/{id}` | GET | Get product details |
| `/api/chat` | POST | Multi-agent chat interface |
| `/api/cart/{user_id}` | GET/POST | Cart management |
| `/api/group-buy/suggestions` | POST | Get group buying recommendations |
| `/api/predict` | POST | Calculate EarthScore for new products |

### Chat API Example
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Show me eco-friendly kitchen products",
    "user_id": "guest"
  }'
```

## 🌍 Environmental Impact

Our platform has facilitated:
- 🌳 **CO2 Reduction** - Track and reduce carbon footprints
- 📦 **60% Less Packaging** - Through smart group buying
- 🔄 **Sustainable Choices** - AI-powered eco-friendly recommendations
- 👥 **Community Impact** - Collective environmental action

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Workflow
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 🏆 Features & Capabilities

- 🤖 **AI-Powered Shopping** - Multi-agent system for intelligent assistance
- 🌟 **EarthScore Rating** - Comprehensive sustainability metrics
- 💚 **Gamified Experience** - Achievements and rewards for eco-friendly shopping
- 👥 **Community Buying** - Save money while saving the planet

## 📈 Future Roadmap

- [ ] Blockchain integration for supply chain transparency
- [ ] AR product scanner for instant EarthScore
- [ ] Voice commerce integration
- [ ] B2B sustainability dashboard
- [ ] Carbon offset marketplace
- [ ] International expansion with localized impact metrics
- [ ] Mobile applications (iOS/Android)

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- **Rishabh Kumar** - Full Stack Developer & AI Integration
- **Nikhil Chauhan** - Full Stack Developer & Backend Architecture
- **Sridhar Vasudevan** - UI/UX Design & Frontend Development

## 🙏 Acknowledgments

- Google Cloud for Gemini API access
- OpenAI for GPT-4 API access
- The open-source community for amazing tools and libraries
- Environmental data providers for sustainability metrics

## 📧 Contact

For questions or collaboration opportunities:
- Email: [iit2022131@iiita.ac.in] [iit2022133@iiita.ac.in] [iit2022163@iiita.ac.in]
- Project Link: [https://github.com/[your-username]/[repo-name]](https://github.com/[your-username]/[repo-name])

---

<p align="center">Made with 💚 for a sustainable future</p>
<p align="center">
  <a href="[Your Live Demo URL]">Visit GreenCart</a> •
  <a href="[Your API Docs URL]">API Docs</a> •
  <a href="#contributing">Contribute</a>
</p>
```

