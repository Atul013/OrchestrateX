# Sahil's MongoDB & Backend API Development Guide
*Team 2: Containerized Database - OrchestrateX Project*

## 🎯 Your Team 2 Responsibilities
As **Sahil** (Team 2: Containerized Database), working with **Jinendran**:

### � **Division of Work:**
- **Jinendran**: Setting up MongoDB database in Docker containers
- **You (Sahil)**: Everything else below ⬇️

### 🗄️ **Your Database Work:**
- Designing database schema and collections
- Managing database security and access controls
- Ensuring data persistence and performance optimization

### 🔧 **Your Backend Development:**
- Implementing backend APIs for CRUD operations
- Creating RESTful endpoints for system integration
- Building secure authentication and authorization
- Documenting database setup and usage instructions

### ⏰ **Project Deadline:**
**Friday, August 29, 2025, 11:59 PM IST** - Working prototype required

## 🚀 **Getting Started: Your Work After Jinendran's Docker Setup**

### **Step 1: Wait for Jinendran's MongoDB Container**
Jinendran will provide you with:
- Running MongoDB Docker container
- Connection details and credentials
- Basic container configuration

### **Step 2: Your Database Schema Design**

Based on OrchestrateX requirements, you'll need these collections:

#### **1. Prompts Collection**
```javascript
// prompts
{
  _id: ObjectId,
  prompt: "String - the actual question/task",
  domain: "String - coding|creative|factual|math|translation|sentiment", 
  difficulty: "String - easy|medium|hard",
  category: "String - specific subcategory",
  language: "String - en|es|fr|etc",
  created_at: "Date",
  metadata: {
    source: "String",
    collector: "String"
  }
}
```

#### **2. AI Responses Collection**
```javascript
// ai_responses  
{
  _id: ObjectId,
  prompt_id: "ObjectId - reference to prompts collection",
  model_name: "String - gpt4|claude|llama|mistral|qwen",
  response: "String - AI model's response",
  response_time: "Number - milliseconds",
  tokens_used: "Number",
  cost: "Number - API cost",
  timestamp: "Date"
}
```

#### **3. Evaluations Collection**
```javascript
// evaluations
{
  _id: ObjectId,
  prompt_id: "ObjectId",
  response_id: "ObjectId", 
  evaluator_id: "String - human evaluator identifier",
  ratings: {
    accuracy: "Number 1-5",
    relevance: "Number 1-5", 
    clarity: "Number 1-5",
    creativity: "Number 1-5"
  },
  overall_score: "Number 1-5",
  comments: "String - optional feedback",
  timestamp: "Date"
}
```

## 🔧 **Backend API Development**

### **Required Endpoints:**

#### **Prompts Management**
```
GET    /api/prompts              # List all prompts (with filters)
POST   /api/prompts              # Create new prompt
GET    /api/prompts/:id          # Get specific prompt
PUT    /api/prompts/:id          # Update prompt
DELETE /api/prompts/:id          # Delete prompt
GET    /api/prompts/domain/:domain # Get prompts by domain
```

#### **AI Responses Management**
```
GET    /api/responses            # List all responses
POST   /api/responses            # Store AI model response
GET    /api/responses/prompt/:id # Get all responses for a prompt
GET    /api/responses/model/:name # Get responses by model
```

#### **Evaluations Management**
```
GET    /api/evaluations          # List all evaluations
POST   /api/evaluations          # Submit evaluation
GET    /api/evaluations/prompt/:id # Get evaluations for prompt
GET    /api/analytics/best-models  # Analytics: best performing models
```

## 📊 **Technology Stack Recommendations**

### **Backend Framework Options:**
1. **Node.js + Express** (JavaScript)
2. **Python + FastAPI** (Python)  
3. **Python + Flask** (Python)

### **MongoDB Integration:**
- **Node.js**: mongoose ODM
- **Python**: pymongo or motor (async)

### **Development Tools:**
- **MongoDB Compass** - GUI for database management
- **Postman** - API testing
- **Docker Desktop** - Container management

## � **Security Requirements**

### **Database Security:**
- Enable MongoDB authentication
- Use environment variables for credentials
- Implement role-based access control
- Set up SSL/TLS for connections

### **API Security:**
- JWT token authentication
- Input validation and sanitization
- Rate limiting
- CORS configuration
- Error handling without information leakage

## 📁 **Project Structure**
```
OrchestrateX/
├── database/
│   ├── docker-compose.yml
│   ├── init-scripts/
│   │   └── setup.js
│   └── schemas/
│       ├── prompts.js
│       ├── responses.js
│       └── evaluations.js
├── backend/
│   ├── app.js (or main.py)
│   ├── routes/
│   │   ├── prompts.js
│   │   ├── responses.js
│   │   └── evaluations.js
│   ├── models/
│   │   ├── Prompt.js
│   │   ├── Response.js
│   │   └── Evaluation.js
│   ├── middleware/
│   │   ├── auth.js
│   │   └── validation.js
│   └── config/
│       └── database.js
└── docs/
    ├── api-documentation.md
    └── setup-instructions.md
```

## ✅ **Week 1 Tasks (Aug 25-29)**

### **Day 1-2: Schema Design & Planning**
- [ ] Coordinate with Jinendran on MongoDB container status
- [ ] Design database collections schema
- [ ] Plan API endpoints and data flow
- [ ] Choose your backend framework

### **Day 3-4: Backend Development**
- [ ] Connect to Jinendran's MongoDB container
- [ ] Implement database models
- [ ] Build CRUD APIs
- [ ] Set up authentication and security

### **Day 5: Integration & Testing**
- [ ] Test all endpoints
- [ ] Document APIs
- [ ] Prepare for team integration
- [ ] Create demo for prototype presentation

## 🤝 **Team Integration Points**

### **With Team 1 (UI - Zayed, Avinash):**
- Provide API endpoints for frontend integration
- Ensure proper CORS and authentication setup
- Document API responses format

### **With Team 3 (Algorithm - Atul):**
- Provide data access for model training
- Create analytics endpoints for algorithm evaluation
- Ensure fast query performance for real-time routing

## � **Success Criteria**
By August 29, 2025, you should have:
- ✅ MongoDB running in Docker
- ✅ Complete database schema implemented
- ✅ All CRUD APIs functional
- ✅ Authentication and security working
- ✅ Documentation complete
- ✅ Ready for team integration

---

**Focus on your database and backend work - that's your core responsibility for OrchestrateX success!** 🚀

*Ready to start with MongoDB Docker setup?*
