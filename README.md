# Sales Forge - AI Sales Intelligence Platform

🚀 **Advanced full-stack sales intelligence platform** with FastAPI backend and React + Tailwind frontend.

## 🎯 **Features**

### **Backend (FastAPI)**
- **4 AI Workflow Endpoints**: Advanced (13 agents), Intermediate (11 agents), Basic (8 agents), Enhanced (user-approved)
- **Mock Strategic Intelligence**: Realistic tactical, strategic, and advanced intelligence simulation
- **Comprehensive APIs**: Health check, workflow info, agent types
- **CORS Enabled**: Ready for frontend integration
- **Production Ready**: Proper error handling, logging, documentation

### **Frontend (React + Tailwind)**
- **Advanced UI**: Modern, responsive design with Tailwind CSS
- **3-Tab Navigation**: Advance-Agents (13), Crew Agents (4), IBM Agents (4)
- **Workflow Menu**: 4 workflow options with detailed descriptions
- **Dynamic Results**: Real-time API integration with beautiful data visualization
- **Agent Information**: Detailed agent capabilities and integration explanations
- **Modular Components**: Clean, maintainable React architecture

## 🏗️ **Architecture**

```
Sales Forge/
├── backend/                 # FastAPI Application
│   ├── application.py       # Main FastAPI app with 4 endpoints
│   └── requirements.txt     # Python dependencies
│
├── frontend/                # React Application  
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── TabNavigation.jsx
│   │   │   ├── WorkflowMenu.jsx
│   │   │   ├── LeadForm.jsx
│   │   │   ├── ResultsDisplay.jsx
│   │   │   └── AgentInfo.jsx
│   │   ├── services/        # API integration
│   │   │   └── api.js
│   │   ├── utils/          # Utility functions
│   │   │   └── formatters.js
│   │   ├── App.jsx         # Main app component
│   │   ├── index.js        # React entry point
│   │   └── index.css       # Tailwind CSS styles
│   ├── public/             # Static assets
│   ├── package.json        # NPM dependencies
│   ├── tailwind.config.js  # Tailwind configuration
│   └── postcss.config.js   # PostCSS configuration
│
└── README.md               # Documentation
```

## 🚀 **Quick Start**

### **🎯 One-Command Startup (Recommended)**

```bash
# Option 1: Simple command
./run.sh

# Option 2: Python script (cross-platform)
python3 start.py

# Option 3: Using npm from frontend directory
cd frontend && npm run start:full
```

**This starts both backend and frontend automatically!**
- **Backend:** http://localhost:8000 (API + Documentation)
- **Frontend:** http://localhost:3000 (Main Application)

### **🔧 Manual Startup (Individual Services)**

**Backend Only:**
```bash
cd backend && python application.py
```

**Frontend Only:**
```bash
cd frontend && npm install && npm start
```

**Both Services:**
```bash
# Terminal 1 - Backend
./start_backend.sh

# Terminal 2 - Frontend
./start_frontend.sh
```

## 🎯 **API Endpoints**

### **Core Endpoints**
- `GET /` - API information
- `GET /api/health` - Health check
- `GET /api/workflows` - Available workflows
- `GET /api/agent-types` - Agent type information

### **Workflow Endpoints**
- `POST /api/agents/advanced` - 13-agent advanced intelligence (10-15 min)
- `POST /api/agents/intermediate` - 11-agent balanced intelligence (7-9 min)  
- `POST /api/agents/basic` - 8-agent fast intelligence (4-5 min)
- `POST /api/agents/enhanced` - User-approved workflow (3-5 min + user interaction)

### **Request Format**
```json
{
  "company_name": "TechFlow Dynamics",
  "contact_name": "Sarah Chen", 
  "contact_email": "sarah.chen@techflow.com",
  "company_size": 850,
  "industry": "Enterprise Software",
  "location": "Austin, TX",
  "annual_revenue": 95000000,
  "pain_points": ["Manual processes", "Data silos"],
  "tech_stack": ["React", "Node.js", "Python"]
}
```

## 🎨 **UI Features**

### **Tab Navigation**
1. **Advance-Agents (13)** - Complete AI intelligence suite with workflow menu
2. **Crew Agents (4)** - Tactical intelligence team information  
3. **IBM Agents (4)** - Strategic business intelligence information

### **Workflow Menu** (Advance-Agents tab only)
- **Advanced (13 agents)** - Complete strategic intelligence
- **Intermediate (11 agents)** - Balanced intelligence with priority advanced features
- **Basic (8 agents)** - Fast core strategic intelligence  
- **Enhanced (Variable)** - User-controlled workflow with email approval

### **Dynamic Results Display**
- **Tactical Intelligence** - Lead scoring, conversion probability, pain points
- **Strategic Intelligence** - ROI modeling, market analysis, implementation planning
- **Advanced Intelligence** - Behavioral profiling, competitive analysis, predictive forecasting
- **Email Preview** - AI-generated personalized outreach emails
- **Recommendations** - Strategic action items and next steps

## 🛠️ **Technology Stack**

### **Backend**
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation and serialization
- **Uvicorn** - ASGI server
- **Python 3.8+** - Programming language

### **Frontend**  
- **React 18** - Modern JavaScript library
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client for API calls
- **Lucide React** - Beautiful icon library
- **Node.js** - JavaScript runtime

## 📊 **Simulated Intelligence Data**

The platform generates realistic mock data for:
- **Lead Scoring** (0.4-0.95 range)
- **Conversion Probabilities** (20-80%)
- **ROI Projections** (2.1x-4.5x multipliers)
- **Market Analysis** ($50M-$500M market sizes)
- **Implementation Timelines** (6-18 months)
- **Risk Assessments** (Low/Medium/High)
- **Behavioral Profiles** (Analytical, Results-driven, etc.)
- **Personalized Email Content** (Subject + body generation)

## 🔧 **Development**

### **Backend Development**
```bash
cd backend
python application.py  # Runs with auto-reload
```

### **Frontend Development**
```bash
cd frontend
npm start  # Runs with hot reload
```

### **Build for Production**
```bash
# Frontend
cd frontend
npm run build

# Backend (using gunicorn or similar)
pip install gunicorn
gunicorn application:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 🎯 **Usage Flow**

1. **Start both backend and frontend servers**
2. **Navigate to http://localhost:3000**  
3. **Choose tab**: Advance-Agents for workflow execution, others for agent information
4. **Select workflow** (in Advance-Agents tab): Advanced, Intermediate, Basic, or Enhanced
5. **Fill lead form** with company information
6. **Click "Analyze Lead"** to run AI analysis
7. **View results** with tactical, strategic, and advanced intelligence
8. **Review email preview** and recommendations

## 🏆 **Production Deployment**

### **Backend Deployment**
- Deploy FastAPI app using Docker, AWS Lambda, or traditional hosting
- Set environment variables for production
- Use production ASGI server (Gunicorn + Uvicorn)

### **Frontend Deployment**
- Build React app: `npm run build`
- Deploy to Vercel, Netlify, AWS S3, or traditional hosting
- Update API base URL in production

## 🎉 **Success!**

You now have a **complete full-stack AI sales intelligence platform** with:
- ✅ Modern FastAPI backend with 4 workflow endpoints
- ✅ Beautiful React + Tailwind frontend
- ✅ Advanced 3-tab navigation system
- ✅ Dynamic workflow menu with 4 options
- ✅ Real-time API integration and results display
- ✅ Comprehensive agent information system
- ✅ Production-ready code architecture

**Ready for enterprise deployment!** 🚀