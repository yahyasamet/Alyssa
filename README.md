# ALYSSA - Autonomous AI Assistant for ADK Voice Assistant
```
ALYSSA Root Manager
├── Network Diagnostics Agent
│   ├── Proactive Event Agent (Technical Appointment Scheduling)
│   ├── Invoice Agent (Billing Support)
│   ├── Tickets Agent (Support Management)
│   └── Email Agent (Appointment Confirmations & Service Notifications)
├── Commercial Agent
│   ├── Plans Agent (Service Plans Management)
│   ├── Email Agent (Promotional Offers & Customer Communications)
│   └── Service Coverage Agent (Zone Management)
├── Database Agent (Customer Data Management)
└── Case Summary Agent (Conversation Context & Workflow Optimization)
```

**ALYSSA** is an autonomous AI assistant that revolutionizes customer support for internet providers by eliminating delays, confusion, and handoffs between commercial and technical departments. This multi-agent system acts as both a smart technician and a billing expert—capable of diagnosing connectivity issues in real time, managing subscriptions, processing payments, and opening support tickets—all through natural voice or text interaction.

Designed to operate 24/7 without human intervention, ALYSSA delivers instant, reliable help to frustrated customers while reducing operational costs and pressure on support teams. For ISPs, it's not just a tool—it's a game-changing solution to modernize service, boost satisfaction, and stay competitive.

## 🚀 Key Features

### 🛠️ Network Diagnostics & Technical Support
- **Real-time Network Diagnostics**: Automated troubleshooting for internet connectivity issues
- **Smart Escalation**: Seamlessly schedules appointments with human technicians when needed
- **Proactive Issue Detection**: Monitors network outages and service disruptions
- **Support Ticket Management**: Creates, tracks, and resolves customer support tickets
- **Appointment Scheduling**: Calendar integration for booking technician visits and follow-ups
- **Service Notifications**: Automated email alerts for outages, maintenance, and resolutions

### 💼 Commercial & Billing Operations
- **Subscription Management**: Handle plan upgrades, downgrades, and new customer onboarding
- **Real-time Billing Support**: Check invoice status, payment processing, and account balance
- **Service Plan Recommendations**: AI-powered plan suggestions based on usage patterns
- **Promotional Campaigns**: Automated email delivery of targeted offers and communications
- **Payment Reminders**: Automated billing notifications and payment confirmations
- **Customer Retention**: Proactive communication for plan optimization and satisfaction

### 📊 Database & Customer Management
- **Customer Profile Management**: Complete user information and service history tracking
- **Service Coverage Analytics**: Zone-based service availability and network performance stats
- **Payment Analytics**: Invoice tracking, payment rates, and overdue account management
- **Multi-language Support**: English and Arabic language support with dynamic switching

### 🤖 Multi-Agent Architecture
- **Manager Agent**: Orchestrates workflow between specialized agents
- **Network Diagnostics Agent**: Technical troubleshooting and issue resolution
- **Commercial Agent**: Plans, pricing, and customer communications
- **Database Agent**: Customer data management and analytics
- **Case Summary Agent**: Conversation context and workflow optimization

## 🏗️ System Architecture

ALYSSA is built using Google's Agent Development Kit (ADK) with a sophisticated multi-agent architecture:

```
ALYSSA Root Manager
├── Network Diagnostics Agent
│   ├── Proactive Event Agent (Appointment Scheduling)
│   ├── Invoice Agent (Billing Support)
│   ├── Tickets Agent (Support Management)
│   └── Email Agent (Communication)
├── Commercial Agent
│   ├── Plans Agent (Service Plans Management)
│   ├── Email Agent (Customer Communications)
│   └── Service Coverage Agent (Zone Management)
├── Database Agent (Customer Data Management)
└── Case Summary Agent (Context Management)
```

### Core Technologies
- **Google ADK**: Advanced agent orchestration and AI capabilities
- **FastAPI**: High-performance web framework for API endpoints
- **Firestore**: Real-time database for customer and billing data
- **WebSocket**: Real-time voice and text communication
- **OAuth 2.0**: Secure authentication for Google services integration

## 🛡️ Enterprise-Grade Capabilities

### Security & Privacy
- **Client ID-based Authentication**: Secure customer identification and data access
- **Data Privacy Controls**: Only access information relevant to authenticated clients
- **OAuth 2.0 Integration**: Secure Google services authentication
- **Audit Trails**: Complete conversation and action logging

### Scalability & Performance
- **24/7 Autonomous Operation**: No human intervention required for standard operations
- **Multi-language Support**: Dynamic language switching (English/Arabic)
- **Real-time Processing**: Instant response to customer queries
- **Background Task Management**: Efficient handling of long-running operations

## 🚀 Quick Start Guide

### 1. Environment Setup

Create a virtual environment and install dependencies:

```powershell
# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Keys

Set up your Google AI Studio API key for Gemini integration:

1. Create or use an existing [Google AI Studio](https://aistudio.google.com/) account
2. Get your Gemini API key from the [API Keys section](https://aistudio.google.com/app/apikeys)
3. Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 3. Database Setup

ALYSSA uses both local JSON files for development and Firestore for production:

**For Development:**
- User data: `app/database/users.json`
- Service plans: `app/database/plans.json`
- Invoices: `app/database/invoices.json`
- Network zones: `app/database/zones.json`
- Support tickets: `app/database/tickets.json`
- Network events: `app/database/events.json`
- Outage information: `app/database/outages.json`

**For Production (Firestore):**
1. Create a [Google Cloud Project](https://console.cloud.google.com/)
2. Enable Firestore API
3. Create a service account and download `serviceAccountKey.json`
4. Place the service account key in the project root
5. Run setup script: `python setup_Firestore.py`
### 4. Launch ALYSSA

Start the ALYSSA autonomous assistant:

```powershell
# Navigate to app directory and start the server
cd app
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Or use the VS Code task:
- Open Command Palette (Ctrl+Shift+P)
- Run "Tasks: Run Task"
- Select "Start Alyssa Assistant"

### 5. Access ALYSSA Interface

- **Web Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 💬 Customer Interaction Examples

### Network Diagnostics
```
Customer: "My internet is not working"
ALYSSA: "I understand how frustrating that must be. Let me help you resolve this quickly. 
         First, let me check your account status and then we'll diagnose the issue."
```

### Billing Support
```
Customer: "What's my current bill status?"
ALYSSA: "Let me check your account. I see you have an invoice of $34.99 due on Jan 15th. 
         Your Standard 50Mbps plan is active and performing well."
```

### Plan Upgrades
```
Customer: "I need faster internet for working from home"
ALYSSA: "Based on your current usage, I recommend our Fiber 100Mbps plan at $49.99/month. 
         It's perfect for video calls and large file uploads. Shall I process the upgrade?"
```

### Technical Appointment Scheduling
```
Customer: "My internet keeps dropping every few hours, nothing seems to fix it"
ALYSSA: "I understand this is frustrating. This sounds like it needs our technical team's attention. 
         Let me schedule a technician visit. I have availability tomorrow between 9-11 AM or 2-4 PM. 
         Which works better for you?"

Customer: "Tomorrow morning works"
ALYSSA: "Perfect! I've scheduled a technician visit for tomorrow 9-11 AM. You'll receive a 
         confirmation email shortly with the technician's contact info and what to expect."
```

### Automated Customer Communications
```
ALYSSA Email: "Hi John, your technician appointment is confirmed for tomorrow 9-11 AM. 
              Your assigned technician Mike will call 15 minutes before arrival. 
              Reference #: TECH-2025-001"

ALYSSA Outage Alert: "We've detected a service interruption in Zone 4 affecting your area. 
                      Our team is working on it. Expected resolution: 2 hours. 
                      We'll update you once service is restored."

ALYSSA Plan Offer: "Based on your usage patterns, you could save $15/month with our new 
                    Fiber Plus plan while getting 2x faster speeds. Reply to upgrade!"
```

## 🔧 Advanced Configuration

### Client ID Authentication
ALYSSA uses client IDs for secure customer identification:
- When provided, ALYSSA personalizes all interactions based on customer profile
- Access to billing, service history, and account-specific information
- Maintains privacy by only accessing data relevant to the authenticated client

### Multi-language Support
- **Default**: English language interface
- **Arabic Support**: Dynamic switching to Arabic (any dialect)
- **Language Detection**: Automatic language switching based on customer input
- **Context Preservation**: Full functionality maintained regardless of language

### Calendar Integration (Appointment Scheduling)
For scheduling technical support appointments with human experts:

1. Enable Google Calendar API in Google Cloud Console
2. Create OAuth 2.0 credentials for desktop application
3. Download and save as `credentials.json`
4. Run authentication setup:

```powershell
python setup_calendar_auth.py
```

**Use Cases:**
- **Technical Escalation**: Schedule appointments when issues require human technician intervention
- **Installation Appointments**: Book technician visits for new service installations
- **Maintenance Windows**: Schedule planned maintenance with customer notifications
- **Follow-up Calls**: Book callback appointments for complex technical issues

### Email Integration (Customer Communications)
For automated customer communication and notifications:

1. Enable Gmail API in Google Cloud Console
2. Create OAuth 2.0 credentials for desktop application
3. Download and save as `credentials.json`
4. Run authentication setup:

```powershell
python setup_gmail_auth.py
```

**Use Cases:**
- **Appointment Confirmations**: Send automated confirmations for scheduled technician visits
- **Service Notifications**: Alert customers about outages, maintenance, or service updates
- **Plan Offers**: Deliver personalized upgrade offers and promotional campaigns
- **Billing Reminders**: Send payment reminders and invoice notifications
- **Resolution Updates**: Notify customers when their support tickets are resolved

## 🛠️ Development & Customization

### Project Structure
```
Alyssa/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── manager/
│   │   ├── agent.py           # Root manager agent
│   │   └── sub_agents/        # Specialized agents
│   ├── database/              # Local JSON data files
│   └── static/                # Web interface assets
├── credentials.json           # Google OAuth credentials
├── serviceAccountKey.json     # Firestore service account
└── requirements.txt           # Python dependencies
```

### Adding Custom Agents
1. Create new agent in `app/manager/sub_agents/`
2. Implement agent logic and tools
3. Register agent in root manager (`app/manager/agent.py`)
4. Add agent to tools list for orchestration

### Database Customization
- **Local Development**: Modify JSON files in `app/database/`
- **Production**: Update Firestore collections
- **Schema Changes**: Update both local and cloud database structures

## 🔍 Troubleshooting

### Common Issues

**Authentication Errors:**
- Verify `.env` file contains correct `GOOGLE_API_KEY`
- Check that Firestore service account key is properly configured
- Ensure all required APIs are enabled in Google Cloud Console

**Performance Issues:**
- Monitor conversation logs in `manager/sub_agents/case_summary_agent/tools/`
- Check database connection and query performance
- Verify sufficient system resources for multi-agent processing

**Agent Communication:**
- Review agent orchestration in `app/manager/agent.py`
- Check tool registration and imports
- Validate agent instruction formatting and tool definitions

### Debugging Tips
- Enable detailed logging in FastAPI with `--log-level debug`
- Use conversation logs to trace agent interactions
- Monitor WebSocket connections for real-time communication issues
- Check Firestore console for database operation errors

## 💼 Business Value & ROI

### For Internet Service Providers
- **Operational Cost Reduction**: 60-80% reduction in customer support costs
- **24/7 Availability**: Continuous service without human intervention
- **Faster Resolution**: Instant response vs. traditional wait times
- **Scalability**: Handle unlimited concurrent customer interactions
- **Consistency**: Uniform service quality across all interactions

### For Customers
- **Immediate Support**: No waiting in queues or being transferred
- **Unified Experience**: Single point of contact for all ISP needs
- **Multilingual Support**: Communication in preferred language
- **Proactive Service**: Issues detected and resolved before customers notice
- **Transparent Billing**: Real-time account status and payment processing

### Competitive Advantages
- **Modern Customer Experience**: Differentiate from traditional ISPs
- **Reduced Churn**: Faster issue resolution improves satisfaction
- **Operational Efficiency**: Support teams focus on complex issues only
- **Data-Driven Insights**: Customer interaction analytics for business intelligence

## 🤝 Support & Community

### Getting Help
- **Documentation**: Comprehensive guides and API references
- **Issue Tracking**: Report bugs and feature requests via GitHub
- **Community**: Connect with other ISP implementers and developers

### Contributing
ALYSSA is designed for enterprise ISP deployment. Contributions welcome for:
- Additional language support
- New agent capabilities
- Performance optimizations
- Integration with popular ISP management systems

### Professional Services
For enterprise deployment, customization, and support:
- Custom agent development
- Integration with existing ISP systems
- Training and onboarding
- Ongoing maintenance and updates

---

**ALYSSA** - Transforming ISP customer support through autonomous AI assistance. Built for the future of telecommunications customer service.
