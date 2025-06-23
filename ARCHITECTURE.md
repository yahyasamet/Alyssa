# ALYSSA - System Architecture Documentation

## 🏗️ Overview

ALYSSA (Autonomous AI Assistant) is built on a sophisticated multi-agent architecture using Google's Agent Development Kit (ADK). The system employs a hierarchical agent orchestration pattern where a root manager coordinates specialized sub-agents to deliver comprehensive ISP customer support capabilities.

## 🎯 Core Design Principles

### 1. **Agent Specialization**
- Each agent has a specific domain of expertise
- Clear separation of concerns between technical and commercial operations
- Modular design enabling independent agent development and testing

### 2. **Autonomous Operation**
- Self-contained decision-making within each agent
- Minimal human intervention required for standard operations
- Intelligent escalation patterns for complex scenarios

### 3. **Scalable Architecture**
- Horizontally scalable multi-agent system
- Stateless agent design with external state management
- Cloud-native deployment capabilities

## 🏛️ System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        ALYSSA ECOSYSTEM                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐    ┌─────────────────────────────────────┐ │
│  │   Web Client    │    │           FastAPI Server           │ │
│  │   (React/JS)    │◄──►│        (Python/WebSocket)          │ │
│  └─────────────────┘    └─────────────────────────────────────┘ │
│                                         │                       │
│                                         ▼                       │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                ROOT MANAGER AGENT                           │ │
│  │              (Orchestration Layer)                         │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                         │                       │
│                         ┌───────────────┼───────────────┐       │
│                         ▼               ▼               ▼       │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐   │
│  │ Network Diag.   │ │  Commercial     │ │   Database      │   │
│  │    Agent        │ │     Agent       │ │    Agent        │   │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘   │
│           │                   │                   │             │
│           ▼                   ▼                   ▼             │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐   │
│  │   Sub-Agents    │ │   Sub-Agents    │ │     Tools       │   │
│  │ • Proactive     │ │ • Plans         │ │ • User Mgmt     │   │
│  │ • Invoice       │ │ • Email         │ │ • Search        │   │
│  │ • Tickets       │ │ • Coverage      │ │ • Analytics     │   │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘   │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                      EXTERNAL SERVICES                         │
│                                                                 │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐   │
│  │   Firestore     │ │ Google Calendar │ │   Gmail API     │   │
│  │   Database      │ │      API        │ │   (Email)       │   │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## 🤖 Agent Architecture

### Root Manager Agent
**Location**: `app/manager/agent.py`

The central orchestrator responsible for:
- **Request Routing**: Analyzing customer requests and delegating to appropriate agents
- **Workflow Coordination**: Managing multi-step processes across agents
- **Context Management**: Maintaining conversation state and customer context
- **Language Support**: Dynamic language switching (English/Arabic)

```python
# Agent Configuration
Agent(
    name="manager",
    model="gemini-2.0-flash-exp",
    tools=[database_agent, network_diagnostics_agent, commercial_agent, case_summary_agent]
)
```

### Network Diagnostics Agent
**Location**: `app/manager/sub_agents/network_diagnostics_agent/agent.py`

Handles technical support and network troubleshooting:

#### Sub-Agents:
1. **Proactive Event Agent** (`proactive_event_agent/`)
   - **Purpose**: Technical appointment scheduling with human experts
   - **Tools**: Calendar integration, event management
   - **Use Cases**: Technician visits, installation appointments, follow-up calls

2. **Invoice Agent** (`invoice_agent/`)
   - **Purpose**: Billing verification and payment status checks
   - **Tools**: Firestore integration, payment analytics
   - **Use Cases**: Service suspension due to non-payment, billing inquiries

3. **Tickets Agent** (`tickets_agent/`)
   - **Purpose**: Support ticket creation and management
   - **Tools**: Ticket lifecycle management, escalation workflows
   - **Use Cases**: Issue tracking, resolution documentation

### Commercial Agent
**Location**: `app/manager/sub_agents/commercial_agent/agent.py`

Manages sales, plans, and customer communications:

#### Sub-Agents:
1. **Plans Agent** (`plans_agent/`)
   - **Purpose**: Service plan management and recommendations
   - **Tools**: Plan database, pricing optimization
   - **Use Cases**: Plan upgrades, new subscriptions, cost optimization

2. **Email Agent** (`emailing_agent/`)
   - **Purpose**: Customer communication and marketing
   - **Tools**: Gmail API, template management
   - **Use Cases**: Promotional offers, service notifications, confirmations

3. **Service Coverage Agent** (`service_coverage_agent/`)
   - **Purpose**: Network zone management and availability checks
   - **Tools**: Zone database, coverage analytics
   - **Use Cases**: Service availability, network performance stats

### Database Agent
**Location**: `app/manager/sub_agents/database_agent/agent.py`

Centralized data management and analytics:

#### Tools:
- **User Management**: Customer profile CRUD operations
- **Search Capabilities**: Multi-field customer search
- **Analytics**: Usage patterns, service statistics
- **Data Integration**: Firestore and local JSON support

### Case Summary Agent
**Location**: `app/manager/sub_agents/case_summary_agent/agent.py`

Conversation context and workflow optimization:
- **Purpose**: Maintain conversation context across agent interactions
- **Tools**: Conversation logging, context summarization
- **Use Cases**: Workflow optimization, agent coordination

## 💾 Data Architecture

### Database Design

#### Local Development (JSON Files)
**Location**: `app/database/`

```
database/
├── users.json          # Customer profiles and subscriptions
├── plans.json          # Service plans and pricing
├── invoices.json       # Billing and payment records
├── zones.json          # Network coverage areas
├── tickets.json        # Support tickets and resolutions
├── events.json         # Network events and incidents
└── outages.json        # Service disruption records
```

#### Production (Firestore)
**Collections Structure**:
```
firestore/
├── users/              # Customer collection
│   ├── {userId}/       # Customer document
│   └── subcollections/ # Orders, history, preferences
├── plans/              # Service plans collection
├── invoices/           # Billing records collection
├── zones/              # Coverage zones collection
├── tickets/            # Support tickets collection
└── events/             # Network events collection
```

### Data Models

#### User Model
```json
{
  "userId": "abc123",
  "fullName": "John Doe",
  "email": "john.doe@gmail.com",
  "phone": "+123456789",
  "zone": "Zone 4",
  "planId": "fiber_100",
  "subscriptionStatus": "active"
}
```

#### Plan Model
```json
{
  "planId": "fiber_100",
  "name": "Fiber 100Mbps",
  "speed": 100,
  "price": 49.99,
  "type": "fiber"
}
```

#### Invoice Model
```json
{
  "invoiceId": "INV-2025-001",
  "userId": "abc123",
  "planId": "fiber_100",
  "amount": 49.99,
  "status": "paid",
  "dueDate": "2025-01-15"
}
```

## 🔧 Technical Stack

### Core Technologies

#### Backend
- **Python 3.8+**: Primary runtime environment
- **FastAPI**: High-performance web framework
- **Google ADK**: Agent orchestration and AI capabilities
- **Gemini 2.0 Flash**: Large language model
- **WebSocket**: Real-time communication
- **Uvicorn**: ASGI server

#### Database & Storage
- **Google Firestore**: Production NoSQL database
- **JSON Files**: Development data storage
- **Firebase Admin SDK**: Database connectivity

#### External Integrations
- **Google Calendar API**: Appointment scheduling
- **Gmail API**: Email communications
- **OAuth 2.0**: Secure authentication

#### Frontend
- **HTML/CSS/JavaScript**: Web interface
- **WebSocket Client**: Real-time communication
- **Audio Processing**: Voice interaction support

### Development Tools
- **VS Code**: Primary IDE with task automation
- **Python Virtual Environment**: Dependency isolation
- **Environment Variables**: Configuration management

## 🔐 Security Architecture

### Authentication & Authorization
- **Client ID-based Authentication**: Secure customer identification
- **OAuth 2.0**: Google services integration
- **Service Account Keys**: Firestore authentication
- **Environment Variables**: API key management

### Data Privacy
- **Client Context Isolation**: Customer data segregation
- **Minimal Data Access**: Need-to-know principle
- **Audit Logging**: Complete interaction tracking
- **Secure Communication**: HTTPS/WSS protocols

### Security Best Practices
- **API Key Rotation**: Regular credential updates
- **Input Validation**: SQL injection prevention
- **Rate Limiting**: DoS attack mitigation
- **Error Handling**: Information disclosure prevention

## 🚀 Deployment Architecture

### Development Environment
```
Local Machine
├── Python Virtual Environment
├── Local JSON Database
├── Environment Configuration (.env)
└── Development Server (localhost:8000)
```

### Production Environment
```
Cloud Infrastructure
├── Application Server (FastAPI + Uvicorn)
├── Google Cloud Firestore
├── Google APIs (Calendar, Gmail)
├── Load Balancer
└── Monitoring & Logging
```

### Scalability Considerations
- **Horizontal Scaling**: Multiple application instances
- **Database Sharding**: Customer data partitioning
- **Caching Layer**: Response time optimization
- **CDN Integration**: Static asset delivery

## 🔄 Agent Communication Patterns

### 1. **Hierarchical Delegation**
```
Root Manager → Specialized Agent → Sub-Agent → Tool
```

### 2. **Cross-Agent Communication**
```
Network Diagnostics ←→ Commercial Agent
         ↓
    Database Agent
```

### 3. **Event-Driven Actions**
```
Customer Request → Context Summary → Agent Selection → Tool Execution → Response
```

## 📊 Performance Characteristics

### Response Times
- **Simple Queries**: < 500ms
- **Complex Workflows**: < 2 seconds
- **Database Operations**: < 1 second
- **External API Calls**: < 3 seconds

### Throughput
- **Concurrent Sessions**: 100+ simultaneous users
- **Request Rate**: 1000+ requests per minute
- **Agent Capacity**: Unlimited parallel processing
- **Database Connections**: Auto-scaling pool

### Resource Requirements
- **CPU**: 2+ cores recommended
- **RAM**: 4GB+ for production workloads
- **Storage**: 10GB+ including logs and data
- **Network**: High-speed internet for API calls

## 🔮 Future Architecture Enhancements

### Planned Improvements
1. **Microservices Architecture**: Individual agent deployment
2. **Message Queue Integration**: Async processing capabilities
3. **Machine Learning Pipeline**: Predictive analytics
4. **Multi-tenancy Support**: Multiple ISP deployment
5. **API Gateway**: Centralized request routing
6. **Container Orchestration**: Kubernetes deployment

### Extensibility Points
- **Custom Agent Development**: Domain-specific extensions
- **Third-party Integrations**: CRM, billing systems
- **Plugin Architecture**: Modular functionality
- **Webhook Support**: External system notifications

---

**ALYSSA Architecture** - Built for scalability, security, and autonomous operation in enterprise ISP environments.
