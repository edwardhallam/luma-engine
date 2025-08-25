import api from '@/utils/api'
import type {
  Deployment,
  DeploymentRequest,
  IaCGenerationRequest,
  IaCGenerationResponse,
  RequirementAnalysisRequest,
  RequirementAnalysisResponse,
  Template,
  Provider,
  SystemHealth,
  SecurityScanResult,
  DeploymentMetrics,
  WorkflowItem,
} from '@/types'

// Health and System APIs
export const healthApi = {
  getHealth: () => api.get('/health'),
  getSystemInfo: () => api.get('/info'),
  getSystemHealth: () => api.get<SystemHealth>('/system/health'),
}

// Requirements Analysis APIs
export const requirementsApi = {
  analyze: (request: RequirementAnalysisRequest) =>
    api.post<RequirementAnalysisResponse>('/requirements/analyze', request),

  refine: (analysisId: string, feedback: any) =>
    api.post<RequirementAnalysisResponse>(`/requirements/refine`, { analysis_id: analysisId, ...feedback }),

  getHistory: (page = 1, pageSize = 20) =>
    api.get(`/requirements/history?page=${page}&page_size=${pageSize}`),

  getTemplates: (category?: string) =>
    api.get(`/requirements/templates${category ? `?category=${category}` : ''}`),

  getSuggestions: (partialRequest: string, context?: string) =>
    api.get(`/requirements/suggestions?partial_request=${encodeURIComponent(partialRequest)}${context ? `&context=${encodeURIComponent(context)}` : ''}`),
}

// IaC Generation APIs
export const iacApi = {
  generate: (request: IaCGenerationRequest) =>
    api.post<IaCGenerationResponse>('/iac/generate', request),

  validate: (code: string, format: string, provider: string) =>
    api.post('/iac/validate', { code, format, provider }),

  getProviders: () =>
    api.get<{ providers: Provider[] }>('/iac/providers'),

  getStatus: () =>
    api.get('/iac/status'),

  getExamples: () =>
    api.get('/iac/examples'),
}

// Deployment APIs
export const deploymentsApi = {
  create: (request: DeploymentRequest) =>
    api.post<Deployment>('/deployments', request),

  list: (page = 1, pageSize = 20, statusFilter?: string, serviceType?: string) => {
    const params = new URLSearchParams({
      page: page.toString(),
      page_size: pageSize.toString(),
    })
    if (statusFilter) params.append('status_filter', statusFilter)
    if (serviceType) params.append('service_type', serviceType)

    return api.get(`/deployments?${params.toString()}`)
  },

  get: (id: string) =>
    api.get<Deployment>(`/deployments/${id}`),

  update: (id: string, data: Partial<DeploymentRequest>) =>
    api.put<Deployment>(`/deployments/${id}`, data),

  delete: (id: string, force = false) =>
    api.delete(`/deployments/${id}?force=${force}`),

  start: (id: string) =>
    api.post<Deployment>(`/deployments/${id}/start`),

  stop: (id: string, graceful = true) =>
    api.post<Deployment>(`/deployments/${id}/stop?graceful=${graceful}`),

  restart: (id: string) =>
    api.post<Deployment>(`/deployments/${id}/restart`),

  getMetrics: (id: string) =>
    api.get<DeploymentMetrics>(`/deployments/${id}/metrics`),

  getLogs: (id: string, lines = 100, follow = false) =>
    api.get(`/deployments/${id}/logs?lines=${lines}&follow=${follow}`),

  getStatus: (id: string) =>
    api.get(`/deployments/${id}/status`),
}

// Template APIs
export const templatesApi = {
  list: (category?: string, provider?: string) => {
    const params = new URLSearchParams()
    if (category) params.append('category', category)
    if (provider) params.append('provider', provider)

    return api.get<Template[]>(`/templates${params.toString() ? `?${params.toString()}` : ''}`)
  },

  get: (id: string) =>
    api.get<Template>(`/templates/${id}`),

  create: (template: Partial<Template>) =>
    api.post<Template>('/templates', template),

  update: (id: string, template: Partial<Template>) =>
    api.put<Template>(`/templates/${id}`, template),

  delete: (id: string) =>
    api.delete(`/templates/${id}`),

  preview: (id: string, variables: Record<string, any>) =>
    api.post(`/templates/${id}/preview`, { variables }),
}

// Security APIs
export const securityApi = {
  scan: (target: string, scanType = 'comprehensive') =>
    api.post<SecurityScanResult>('/security/scan', { target, scan_type: scanType }),

  getScanResults: (scanId: string) =>
    api.get<SecurityScanResult>(`/security/scan/${scanId}`),

  getStatus: () =>
    api.get('/security/status'),

  getAuditReport: () =>
    api.get('/security/audit'),
}

// Monitoring APIs
export const monitoringApi = {
  getMetrics: (timeRange = '1h') =>
    api.get(`/monitoring/metrics?range=${timeRange}`),

  getAlerts: (active = true) =>
    api.get(`/monitoring/alerts?active=${active}`),

  getDashboard: (dashboardType = 'overview') =>
    api.get(`/monitoring/dashboard/${dashboardType}`),
}

// GitHub Project Workflow APIs (mock for now - would integrate with GitHub API)
export const workflowApi = {
  getWorkflowItems: () => {
    // Mock data based on the GitHub project items we saw earlier
    const mockItems: WorkflowItem[] = [
      {
        id: 'PVTI_lAHOAJrT-84BA13-zgdzwnk',
        title: 'Implement Pre-commit Security Hooks for Sensitive Data Protection',
        status: 'Review',
        priority: 'High',
        size: 'Small',
        estimate: 3,
        description: 'Implement comprehensive pre-commit security measures and runtime security monitoring to prevent accidental commits of sensitive data.',
        repository: 'edwardhallam/luma-engine',
        assignees: ['edwardhallam'],
      },
      {
        id: 'PVTI_lAHOAJrT-84BA13-zgdwyc4',
        title: 'Enhanced IaC Generation: Pulumi/CDK Integration Beyond Jinja2 Templates',
        status: 'Review',
        priority: 'High',
        size: 'Large',
        estimate: 8,
        description: 'Enhanced approach to IaC generation beyond Jinja2 templates, incorporating modern type-safe programmatic infrastructure definition tools.',
        repository: 'edwardhallam/luma-engine',
        assignees: ['edwardhallam'],
      },
      {
        id: 'PVTI_lAHOAJrT-84BA13-zgdwydA',
        title: 'Build IaC Generation Service with Validation',
        status: 'Ready',
        priority: 'High',
        size: 'Large',
        estimate: 8,
        description: 'Implement the core Infrastructure as Code generation service that converts analyzed requirements into validated OpenTofu/Terraform configurations.',
        repository: 'edwardhallam/luma-engine',
        assignees: ['edwardhallam'],
      },
      {
        id: 'PVTI_lAHOAJrT-84BA13-zgdwyzw',
        title: 'Implement Temporal Workflow Orchestration',
        status: 'Ready',
        priority: 'Medium',
        size: 'Large',
        estimate: 13,
        description: 'Integrate Temporal workflow engine for reliable, long-running infrastructure deployment orchestration.',
        repository: 'edwardhallam/luma-engine',
        assignees: ['edwardhallam'],
      },
    ]

    return Promise.resolve({ data: mockItems })
  },

  updateWorkflowItem: (id: string, updates: Partial<WorkflowItem>) =>
    Promise.resolve({ data: { id, ...updates } }),
}
