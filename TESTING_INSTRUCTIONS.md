# ALYSSA Testing Instructions

## 🧪 Comprehensive Testing Guide for Multi-Agent AI System

This document provides complete testing instructions for ALYSSA (Autonomous Language-enabled Year-round Service Support Assistant), the multi-agent AI system built with Google's Agent Development Kit for ISP customer support automation.

## 📋 Prerequisites

### System Requirements
- **Python 3.8+** installed
- **Google Cloud Project** with appropriate APIs enabled
- **Valid Google Service Account** with required permissions
- **Firestore Database** properly configured
- **Internet connection** for Google API access

### Required API Access
- ✅ **Firestore API** - Customer data management
- ✅ **Calendar API** - Appointment scheduling
- ✅ **Gmail API** - Email automation
- ✅ **Gemini API** - AI model access
- ✅ **Agent Development Kit** - Multi-agent orchestration

### Environment Setup
```bash
# 1. Clone and navigate to project directory
cd "c:\Users\Hama\3D Objects\Alyssa"

# 2. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create a .env file in the project root with:
# GOOGLE_API_KEY=your_gemini_api_key_here

# 5. Verify Google Cloud credentials
# Ensure serviceAccountKey.json is in root directory
# Ensure credentials.json is configured for OAuth

# 6. Test database connectivity
python setup_Firestore.py

# 7. Verify Google API authentication
python setup_calendar_auth.py
python setup_gmail_auth.py
```

## 🚀 Starting the Application

### Method 1: Using VS Code Task (Recommended)
```bash
# In VS Code Terminal
# Use the predefined task: "Start Alyssa Assistant"
# This runs: cd app && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Method 2: Manual Startup (Primary Method)
```powershell
# Navigate to app directory and start the server
cd app
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Method 3: Background Process
```powershell
# Start as background service
python -m uvicorn main:app --host 0.0.0.0 --port 8000 &
```

### Verify Startup
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **WebSocket Test**: http://localhost:8000 (main interface)

## 🎙️ Customer Interaction Guide (Local and Hosted)

### How to Start a Conversation
Communicating with ALYSSA is designed to be as simple as talking to a person:

1. **Press the Microphone Button**: Locate the large microphone icon on your screen. Press it down to activate ALYSSA.
2. **Speak Naturally**: There's no need for robotic commands. Just state your problem or question clearly in your own words. When you're finished speaking, simply release the button.

### Understanding ALYSSA's Status
As ALYSSA works to resolve your issue, you'll see her status change. This lets you know exactly what's happening "under the hood":

- **🔵 Thinking...**: ALYSSA is processing what you said, understanding your intent and the core of your request.
- **⚙️ Consulting Agents...**: This is where the magic happens. ALYSSA is communicating with her team of specialized sub-agents (like the Billing, Technical, or Commercial agents) to gather information and find the best solution.
- **🗣️ Speaking...**: ALYSSA is formulating and delivering her response. You will hear her speak, and you'll also see a real-time transcript of the conversation on your screen.

### What Can You Ask ALYSSA?
You can ask ALYSSA about almost anything related to your account. The more naturally you speak, the better she can help:

**For Technical Issues:**
- "My internet isn't working."
- "The connection keeps dropping during video calls."
- "My WiFi is very slow today."

**For Billing Questions:**
- "What's my current bill amount?"
- "Can you send my latest invoice to my email?"
- "Why is my bill higher this month?"

**For Service Plans & Offers:**
- "I need faster internet for working from home."
- "What are my upgrade options?"
- "Are there any new offers in my zone?"

**For Appointments:**
- "I need a technician to come fix my internet."
- "Can someone come check my connection?"
- "Schedule a service appointment with an expert."

## 🧪 Testing Scenarios

### 1. **Basic Functionality Tests**

#### Test 1.1: Agent System Initialization
```python
# Expected: All agents load successfully
curl -X GET "http://localhost:8000/health"
# Response should show all agents: manager, database_agent, network_diagnostics_agent, etc.
```

#### Test 1.2: Database Connectivity
```python
# Test Firestore connection
curl -X GET "http://localhost:8000/api/test/database"
# Expected: {"status": "connected", "collections": ["users", "plans", "invoices", ...]}
```

#### Test 1.3: Google API Authentication
```python
# Test Calendar API
curl -X GET "http://localhost:8000/api/test/calendar"
# Expected: {"status": "authenticated", "calendar_access": true}

# Test Gmail API
curl -X GET "http://localhost:8000/api/test/gmail"
# Expected: {"status": "authenticated", "gmail_access": true}
```

### 2. **Multi-Agent Orchestration Tests**

#### Test 2.1: Root Manager Agent Routing
**Scenario**: Test intelligent agent selection based on customer input

```javascript
// WebSocket connection test
const ws = new WebSocket('ws://localhost:8000/ws/test_customer_001');

// Test technical inquiry routing
ws.send(JSON.stringify({
    "message": "My internet isn't working",
    "customer_id": "test_customer_001"
}));
// Expected: Routes to network_diagnostics_agent
```

#### Test 2.2: Cross-Agent Collaboration
**Scenario**: Test billing verification during technical troubleshooting

```javascript
// Test scenario: Technical issue with billing check
ws.send(JSON.stringify({
    "message": "My connection keeps dropping during video calls",
    "customer_id": "test_customer_002"
}));
// Expected: 
// 1. Network diagnostics agent activated
// 2. Invoice agent checks billing status
// 3. Appropriate response based on billing status
```

#### Test 2.3: Commercial Agent Activation
**Scenario**: Test plan upgrade workflow

```javascript
ws.send(JSON.stringify({
    "message": "I work from home now and need faster internet",
    "customer_id": "test_customer_003"
}));
// Expected:
// 1. Routes to commercial_agent
// 2. Database agent retrieves current plan
// 3. Plans agent recommends upgrades
// 4. Email agent sends proposal
```

### 3. **Database Agent Tests**

#### Test 3.1: Customer Data Retrieval
```python
# Test user lookup
curl -X POST "http://localhost:8000/api/database/get_user" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_customer_001"}'
# Expected: Complete customer profile with billing info
```

#### Test 3.2: Customer Search Functionality
```python
# Test customer search
curl -X POST "http://localhost:8000/api/database/search_users" \
  -H "Content-Type: application/json" \
  -d '{"query": "john", "filters": {"zone": "Zone1"}}'
# Expected: Array of matching customers
```

#### Test 3.3: User Addition
```python
# Test adding new customer
curl -X POST "http://localhost:8000/api/database/add_user" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Customer",
    "email": "test@example.com",
    "phone": "+1234567890",
    "zone": "Zone1",
    "plan": "basic"
  }'
# Expected: New customer created with generated ID
```

### 4. **Network Diagnostics Agent Tests**

#### Test 4.1: Technical Troubleshooting Flow
**Scenario**: Customer reports slow internet

```javascript
ws.send(JSON.stringify({
    "message": "My internet is really slow today",
    "customer_id": "test_customer_004"
}));
// Expected Workflow:
// 1. Invoice agent checks billing
// 2. If billing OK, diagnostic questions
// 3. Potential technician scheduling
// 4. Email confirmation
```

#### Test 4.2: Proactive Event Management
**Scenario**: Scheduled technician visit

```python
# Test appointment creation
curl -X POST "http://localhost:8000/api/agents/proactive_event/create_appointment" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "test_customer_005",
    "issue_type": "connection_drops",
    "preferred_time": "2025-06-24T14:00:00Z"
  }'
# Expected: Calendar event created, email sent
```

#### Test 4.3: Support Ticket Management
```python
# Test ticket creation
curl -X POST "http://localhost:8000/api/agents/tickets/create_ticket" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "test_customer_006",
    "issue_type": "technical",
    "description": "Intermittent connection issues",
    "priority": "medium"
  }'
# Expected: Support ticket created and tracked
```

### 5. **Commercial Agent Tests**

#### Test 5.1: Plan Management
```python
# Test plan recommendations
curl -X POST "http://localhost:8000/api/agents/plans/recommend_plan" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "test_customer_007",
    "usage_requirements": "high_bandwidth",
    "budget_range": "premium"
  }'
# Expected: Personalized plan recommendations
```

#### Test 5.2: Email Automation
```python
# Test personalized email sending
curl -X POST "http://localhost:8000/api/agents/email/send_email" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "test_customer_008",
    "template_type": "plan_upgrade_proposal",
    "dynamic_data": {
      "current_plan": "basic",
      "recommended_plan": "premium",
      "savings": "$20/month"
    }
  }'
# Expected: Personalized email sent via Gmail API
```

#### Test 5.3: Service Coverage Analysis
```python
# Test zone coverage check
curl -X POST "http://localhost:8000/api/agents/coverage/check_coverage" \
  -H "Content-Type: application/json" \
  -d '{
    "address": "123 Test Street, Test City",
    "service_type": "fiber"
  }'
# Expected: Coverage availability and speed information
```

### 6. **Advanced Multi-Language Tests**

#### Test 6.1: Language Detection and Switching
```javascript
// Test Arabic input
ws.send(JSON.stringify({
    "message": "الإنترنت لا يعمل",
    "customer_id": "test_customer_009"
}));
// Expected: Detects Arabic, responds in Arabic

// Test English follow-up
ws.send(JSON.stringify({
    "message": "Can you switch to English please?",
    "customer_id": "test_customer_009"
}));
// Expected: Switches to English while maintaining context
```

#### Test 6.2: Mixed Language Input
```javascript
ws.send(JSON.stringify({
    "message": "My internet speed is only 10 ميجابايت per second",
    "customer_id": "test_customer_010"
}));
// Expected: Understands mixed Arabic/English input correctly
```

### 7. **Performance and Load Tests**

#### Test 7.1: Concurrent Connections
```python
# Simulate 10 concurrent WebSocket connections
import asyncio
import websockets

async def test_concurrent_connections():
    connections = []
    for i in range(10):
        uri = f"ws://localhost:8000/ws/load_test_customer_{i}"
        connections.append(await websockets.connect(uri))
    
    # Send messages simultaneously
    tasks = []
    for i, ws in enumerate(connections):
        message = f"Test message from customer {i}"
        tasks.append(ws.send(json.dumps({"message": message})))
    
    await asyncio.gather(*tasks)
    
    # Verify responses
    for ws in connections:
        response = await ws.recv()
        print(f"Response: {response}")

# Expected: All connections handled successfully with <2s response time
```

#### Test 7.2: Database Performance
```python
# Test rapid database queries
import time

start_time = time.time()
for i in range(100):
    response = requests.post(
        "http://localhost:8000/api/database/get_user",
        json={"user_id": f"test_customer_{i % 10}"}
    )
end_time = time.time()

average_response_time = (end_time - start_time) / 100
# Expected: Average response time < 100ms
```

### 8. **Error Handling and Edge Cases**

#### Test 8.1: Invalid Customer ID
```python
curl -X POST "http://localhost:8000/api/database/get_user" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "nonexistent_customer"}'
# Expected: Graceful error handling with helpful message
```

#### Test 8.2: Network Outage Simulation
```python
# Test behavior when external APIs are unavailable
# Temporarily block internet access and test agent responses
# Expected: Graceful degradation, cached data usage, error recovery
```

#### Test 8.3: Malformed Input Handling
```javascript
// Test invalid JSON
ws.send("invalid json data");
// Expected: Error handling without system crash

// Test empty message
ws.send(JSON.stringify({"message": "", "customer_id": "test"}));
// Expected: Appropriate prompt for clarification
```

### 9. **Integration Tests**

#### Test 9.1: End-to-End Customer Journey
**Complete Workflow Test**:

```javascript
// 1. Customer reports issue
ws.send(JSON.stringify({
    "message": "My internet has been slow for 3 days",
    "customer_id": "integration_test_001"
}));

// 2. Follow diagnostic questions
ws.send(JSON.stringify({
    "message": "Yes, I've tried restarting my router",
    "customer_id": "integration_test_001"
}));

// 3. Request technician visit
ws.send(JSON.stringify({
    "message": "I'd like to schedule a technician visit",
    "customer_id": "integration_test_001"
}));

// 4. Confirm appointment
ws.send(JSON.stringify({
    "message": "Tomorrow at 2 PM works for me",
    "customer_id": "integration_test_001"
}));

// Expected Complete Flow:
// 1. Issue logged → network_diagnostics_agent
// 2. Billing verified → invoice_agent
// 3. Diagnostics performed → technical troubleshooting
// 4. Appointment scheduled → proactive_event_agent
// 5. Calendar event created → Google Calendar API
// 6. Confirmation email sent → emailing_agent → Gmail API
// 7. Support ticket created → tickets_agent
// 8. Case summary generated → case_summary_agent
```

#### Test 9.2: Plan Upgrade Complete Workflow
```javascript
// Complete commercial workflow test
ws.send(JSON.stringify({
    "message": "I need faster internet for my home office",
    "customer_id": "integration_test_002"
}));
// Expected: Plan analysis → recommendations → email proposal → confirmation
```

## 📊 Monitoring and Analytics

### Real-time Performance Monitoring
```python
# Check agent performance metrics
curl -X GET "http://localhost:8000/api/monitoring/agent_metrics"
# Expected: Response times, success rates, error counts for each agent

# Check system health
curl -X GET "http://localhost:8000/api/monitoring/system_health"
# Expected: Memory usage, active connections, API status
```

### Conversation Analytics
```python
# Get conversation summaries
curl -X GET "http://localhost:8000/api/analytics/conversation_summary/test_customer_001"
# Expected: Complete conversation history, agent handoffs, resolution status
```

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Issue 1: WebSocket Connection Failures
**Symptoms**: Cannot establish WebSocket connection
**Solutions**:
1. Verify server is running on port 8000
2. Check firewall settings
3. Ensure WebSocket route is properly configured

#### Issue 2: Google API Authentication Errors
**Symptoms**: 401/403 errors when accessing Calendar/Gmail
**Solutions**:
1. Verify `credentials.json` is properly configured
2. Check OAuth scope permissions
3. Refresh authentication tokens

#### Issue 3: Firestore Connection Issues
**Symptoms**: Database operations failing
**Solutions**:
1. Verify `serviceAccountKey.json` is present and valid
2. Check Firestore rules and permissions
3. Ensure project ID is correctly configured

#### Issue 4: Agent Response Delays
**Symptoms**: Slow response times (>5 seconds)
**Solutions**:
1. Check Gemini API rate limits
2. Verify database indexing
3. Monitor memory usage and optimize

## ✅ Test Completion Checklist

### Basic Functionality ✅
- [ ] Server starts successfully
- [ ] All agents initialize properly
- [ ] Database connectivity confirmed
- [ ] Google APIs authenticated

### Agent Orchestration ✅
- [ ] Root manager routes correctly
- [ ] Cross-agent collaboration works
- [ ] Context sharing functional
- [ ] Error handling graceful

### Feature Testing ✅
- [ ] Customer data operations work
- [ ] Appointment scheduling functional
- [ ] Email automation working
- [ ] Multi-language support active

### Performance Testing ✅
- [ ] Concurrent connections handled
- [ ] Response times under 2 seconds
- [ ] Memory usage stable
- [ ] Error recovery functional

### Integration Testing ✅
- [ ] End-to-end workflows complete
- [ ] Google services integration working
- [ ] Real customer scenarios tested
- [ ] Edge cases handled properly

## 📞 Support and Documentation

For additional testing support or issues:
- **Technical Documentation**: `README.md`
- **Architecture Details**: `ARCHITECTURE.md`
- **Project Background**: `About the project.md`
- **Business Context**: `BUSINESS_CASE.md`

---

**Note**: This testing guide covers all major functionality of the ALYSSA multi-agent system. For production deployment, additional security testing, load testing, and compliance validation may be required.
