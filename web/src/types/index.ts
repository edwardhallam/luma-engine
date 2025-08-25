// API Response Types
export interface ApiResponse<T = any> {
  success: boolean
  data?: T
  error?: string
  message?: string
}

// Deployment Types
export interface Deployment {
  id: string
  name: string
  status: 'pending' | 'running' | 'completed' | 'failed' | 'stopped'
  provider: string
  environment: 'development' | 'staging' | 'production'
  created_at: string
  updated_at: string
  requirements: string
  infrastructure_code?: string
  validation_results?: ValidationResult[]
  cost_estimate?: CostEstimate
  metrics?: DeploymentMetrics
}

export interface DeploymentRequest {
  name: string
  requirements: string
  provider: string
  environment: string
  format?: string
  enable_validation?: boolean
  enable_optimization?: boolean
}

// IaC Types
export interface IaCGenerationRequest {
  requirements: string
  provider: string
  format: string
  project_name: string
  environment: string
  enable_validation?: boolean
  enable_optimization?: boolean
}

export interface IaCGenerationResponse {
  success: boolean
  infrastructure_code: string
  validation_results: ValidationResult[]
  cost_estimate?: CostEstimate
  processing_time: number
  error?: string
}

export interface ValidationResult {
  valid: boolean
  error_count: number
  warning_count: number
  issues: ValidationIssue[]
}

export interface ValidationIssue {
  type: 'error' | 'warning' | 'info'
  message: string
  line?: number
  column?: number
  rule?: string
}

// Cost Types
export interface CostEstimate {
  total_monthly_cost: number
  breakdown: CostBreakdown[]
  currency: string
  confidence: number
}

export interface CostBreakdown {
  resource_type: string
  resource_name: string
  monthly_cost: number
  unit_cost?: number
  units?: number
}

// Metrics Types
export interface DeploymentMetrics {
  deployment_id: string
  cpu_usage: number
  memory_usage: number
  disk_usage: number
  network_in: number
  network_out: number
  uptime: number
  timestamp: string
}

// Requirements Types
export interface RequirementAnalysisRequest {
  requirements: string
  context?: string
  target_platform?: string
  environment?: string
}

export interface RequirementAnalysisResponse {
  id: string
  analysis: RequirementAnalysis
  confidence_score: number
  processing_time: number
  suggestions?: string[]
}

export interface RequirementAnalysis {
  infrastructure_components: InfrastructureComponent[]
  networking_requirements: NetworkingRequirement[]
  security_requirements: SecurityRequirement[]
  storage_requirements: StorageRequirement[]
  compute_requirements: ComputeRequirement[]
  monitoring_requirements: MonitoringRequirement[]
}

export interface InfrastructureComponent {
  type: string
  name: string
  specifications: Record<string, any>
  dependencies?: string[]
}

export interface NetworkingRequirement {
  type: string
  configuration: Record<string, any>
}

export interface SecurityRequirement {
  type: string
  configuration: Record<string, any>
}

export interface StorageRequirement {
  type: string
  size: string
  configuration: Record<string, any>
}

export interface ComputeRequirement {
  type: string
  cpu: string
  memory: string
  configuration: Record<string, any>
}

export interface MonitoringRequirement {
  type: string
  configuration: Record<string, any>
}

// Template Types
export interface Template {
  id: string
  name: string
  description: string
  category: string
  provider: string
  template_content: string
  variables: TemplateVariable[]
  created_at: string
  updated_at: string
}

export interface TemplateVariable {
  name: string
  type: string
  description: string
  default_value?: any
  required: boolean
}

// Provider Types
export interface Provider {
  name: string
  display_name: string
  description: string
  supported_formats: string[]
  cost_tier: string
}

// Project Workflow Types
export interface WorkflowItem {
  id: string
  title: string
  status: 'Review' | 'Ready' | 'In Progress' | 'Done'
  priority: 'High' | 'Medium' | 'Low'
  size: 'Small' | 'Medium' | 'Large'
  estimate: number
  description: string
  repository: string
  assignees: string[]
}

// Security Types
export interface SecurityScanResult {
  scan_id: string
  status: 'completed' | 'running' | 'failed'
  findings: SecurityFinding[]
  timestamp: string
}

export interface SecurityFinding {
  severity: 'critical' | 'high' | 'medium' | 'low' | 'info'
  type: string
  title: string
  description: string
  file?: string
  line?: number
  remediation?: string
}

// Monitoring Types
export interface SystemHealth {
  status: 'healthy' | 'degraded' | 'unhealthy'
  services: ServiceStatus[]
  timestamp: string
}

export interface ServiceStatus {
  name: string
  status: 'up' | 'down' | 'degraded'
  response_time?: number
  error_rate?: number
}
