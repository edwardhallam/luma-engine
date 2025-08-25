# LumaEngine Web Interface

Modern React-based web interface for the LumaEngine AI Infrastructure Orchestration Platform.

## Features

- **Dashboard Overview**: Real-time system status, metrics, and deployment statistics
- **Project Workflow Board**: Kanban-style board for managing development tasks
- **Requirements Analysis**: Natural language to infrastructure requirements conversion
- **IaC Generation**: Generate infrastructure code with validation and cost estimation
- **Template Management**: Manage reusable infrastructure templates
- **Deployment Monitoring**: Monitor active deployments with real-time metrics
- **Security & Compliance**: Security scanning, compliance tracking, and policy management
- **Cost Optimization**: Cost analysis and optimization recommendations

## Tech Stack

- **Frontend**: React 18 with TypeScript
- **UI Framework**: Material-UI (MUI) v5
- **State Management**: React Query for server state
- **Code Editor**: Monaco Editor (VS Code editor)
- **Charts**: Recharts
- **Drag & Drop**: React Beautiful DnD
- **Build Tool**: Vite
- **Routing**: React Router v6

## Development

### Prerequisites

- Node.js 18+
- npm or yarn

### Setup

1. Install dependencies:
```bash
cd web
npm install
```

2. Start development server:
```bash
npm run dev
```

The web interface will be available at http://localhost:3000

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## API Integration

The web interface connects to the LumaEngine FastAPI backend at `http://localhost:8000/api/v1`. The proxy configuration in `vite.config.ts` automatically forwards API calls during development.

## Architecture

```
src/
├── components/          # Reusable components
│   └── Layout.tsx      # Main layout with navigation
├── pages/              # Page components
│   ├── Dashboard.tsx
│   ├── WorkflowBoard.tsx
│   ├── RequirementAnalysis.tsx
│   ├── IaCGeneration.tsx
│   ├── TemplateManagement.tsx
│   ├── DeploymentMonitoring.tsx
│   ├── SecurityCompliance.tsx
│   └── CostOptimization.tsx
├── services/           # API service functions
│   └── api.ts
├── types/              # TypeScript type definitions
│   └── index.ts
├── utils/              # Utility functions
│   └── api.ts         # Axios configuration
├── App.tsx            # Main application component
└── main.tsx           # Application entry point
```

## Key Components

### Dashboard
- System health overview
- Deployment statistics
- Performance charts
- Quick actions

### Workflow Board
- Drag-and-drop kanban board
- Task status management
- GitHub integration
- Progress tracking

### Requirements Analysis
- Natural language input
- AI-powered analysis
- Multi-agent system results
- Infrastructure recommendations

### IaC Generation
- Code generation from requirements
- Multi-provider support (Terraform, Pulumi, etc.)
- Real-time validation
- Cost estimation

### Template Management
- Template library
- Version control
- Variable management
- Preview functionality

### Deployment Monitoring
- Real-time deployment status
- Resource metrics
- Log viewing
- Deployment controls

### Security & Compliance
- Security score tracking
- Vulnerability scanning
- Compliance monitoring
- Finding details

### Cost Optimization
- Cost breakdown analysis
- Optimization recommendations
- Savings tracking
- Budget monitoring

## Contributing

1. Follow the existing code style and patterns
2. Use TypeScript for type safety
3. Write responsive components using MUI's Grid system
4. Implement proper error handling
5. Add loading states for async operations
6. Use React Query for server state management

## Deployment

Build the production bundle:
```bash
npm run build
```

The built files will be in the `dist/` directory, ready for deployment to any static hosting service.
