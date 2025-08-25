import { useState } from 'react'
import { useMutation, useQuery } from 'react-query'
import {
  Box,
  Typography,
  Paper,
  Grid,
  TextField,
  Button,
  Card,
  CardContent,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Switch,
  FormControlLabel,
  Alert,
  Tabs,
  Tab,
  Chip,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  CircularProgress,
  LinearProgress,
} from '@mui/material'
import {
  Code,
  CheckCircle,
  Error,
  Warning,
  Download,
  Visibility,
  Security,
  TrendingUp,
  Build,
} from '@mui/icons-material'
import Editor from '@monaco-editor/react'
import { iacApi } from '@/services/api'
import type { IaCGenerationRequest, IaCGenerationResponse, ValidationResult } from '@/types'

interface TabPanelProps {
  children?: React.ReactNode
  index: number
  value: number
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ py: 2 }}>{children}</Box>}
    </div>
  )
}

export default function IaCGeneration() {
  const [activeTab, setActiveTab] = useState(0)
  const [request, setRequest] = useState<IaCGenerationRequest>({
    requirements: '',
    provider: 'proxmox',
    format: 'terraform',
    project_name: '',
    environment: 'development',
    enable_validation: true,
    enable_optimization: true,
  })
  const [generationResult, setGenerationResult] = useState<IaCGenerationResponse | null>(null)
  const [validationResult, setValidationResult] = useState<ValidationResult | null>(null)

  const { data: providers } = useQuery('iacProviders', iacApi.getProviders)
  const { data: examples } = useQuery('iacExamples', iacApi.getExamples)

  const generateMutation = useMutation(
    (req: IaCGenerationRequest) => iacApi.generate(req),
    {
      onSuccess: (response) => {
        setGenerationResult(response.data)
        if (response.data.validation_results) {
          setValidationResult(response.data.validation_results[0])
        }
      },
    }
  )

  const validateMutation = useMutation(
    ({ code, format, provider }: { code: string; format: string; provider: string }) =>
      iacApi.validate(code, format, provider),
    {
      onSuccess: (response) => {
        setValidationResult(response.data)
      },
    }
  )

  const handleGenerate = () => {
    if (!request.requirements.trim() || !request.project_name.trim()) return
    generateMutation.mutate(request)
  }

  const handleValidate = () => {
    if (!generationResult?.infrastructure_code) return
    validateMutation.mutate({
      code: generationResult.infrastructure_code,
      format: request.format,
      provider: request.provider,
    })
  }

  const handleUseExample = (example: any) => {
    setRequest({
      ...request,
      requirements: example.request.requirements,
      provider: example.request.provider,
      format: example.request.format,
      project_name: example.request.project_name,
      environment: example.request.environment,
    })
  }

  const handleDownload = () => {
    if (!generationResult?.infrastructure_code) return

    const blob = new Blob([generationResult.infrastructure_code], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${request.project_name}.${request.format === 'terraform' ? 'tf' : 'py'}`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const renderValidationIssues = (validation: ValidationResult) => {
    if (!validation.issues || validation.issues.length === 0) {
      return (
        <Alert severity="success" sx={{ mb: 2 }}>
          <Box display="flex" alignItems="center" gap={1}>
            <CheckCircle />
            <Typography>All validation checks passed!</Typography>
          </Box>
        </Alert>
      )
    }

    return (
      <Box>
        <Box display="flex" gap={2} mb={2}>
          {validation.error_count > 0 && (
            <Chip
              icon={<Error />}
              label={`${validation.error_count} errors`}
              color="error"
              size="small"
            />
          )}
          {validation.warning_count > 0 && (
            <Chip
              icon={<Warning />}
              label={`${validation.warning_count} warnings`}
              color="warning"
              size="small"
            />
          )}
        </Box>

        <List>
          {validation.issues.map((issue, index) => (
            <ListItem key={index} divider>
              <ListItemIcon>
                {issue.type === 'error' ? (
                  <Error color="error" />
                ) : issue.type === 'warning' ? (
                  <Warning color="warning" />
                ) : (
                  <CheckCircle color="info" />
                )}
              </ListItemIcon>
              <ListItemText
                primary={issue.message}
                secondary={
                  <Box>
                    {issue.line && <Typography variant="caption">Line {issue.line}</Typography>}
                    {issue.rule && (
                      <Chip label={issue.rule} size="small" variant="outlined" sx={{ ml: 1 }} />
                    )}
                  </Box>
                }
              />
            </ListItem>
          ))}
        </List>
      </Box>
    )
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom fontWeight="bold">
        Infrastructure as Code Generation
      </Typography>
      <Typography variant="body1" color="textSecondary" mb={3}>
        Generate production-ready infrastructure code from your requirements
      </Typography>

      <Grid container spacing={3}>
        {/* Configuration Panel */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Configuration
            </Typography>

            <TextField
              fullWidth
              label="Project Name"
              value={request.project_name}
              onChange={(e) => setRequest({ ...request, project_name: e.target.value })}
              sx={{ mb: 2 }}
            />

            <TextField
              fullWidth
              multiline
              rows={4}
              label="Requirements"
              placeholder="Describe your infrastructure needs..."
              value={request.requirements}
              onChange={(e) => setRequest({ ...request, requirements: e.target.value })}
              sx={{ mb: 2 }}
            />

            <Grid container spacing={2} mb={2}>
              <Grid item xs={6}>
                <FormControl fullWidth>
                  <InputLabel>Provider</InputLabel>
                  <Select
                    value={request.provider}
                    onChange={(e) => setRequest({ ...request, provider: e.target.value })}
                  >
                    {providers?.data?.providers?.map((provider) => (
                      <MenuItem key={provider.name} value={provider.name}>
                        {provider.display_name}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={6}>
                <FormControl fullWidth>
                  <InputLabel>Format</InputLabel>
                  <Select
                    value={request.format}
                    onChange={(e) => setRequest({ ...request, format: e.target.value })}
                  >
                    <MenuItem value="terraform">Terraform</MenuItem>
                    <MenuItem value="opentofu">OpenTofu</MenuItem>
                    <MenuItem value="pulumi">Pulumi</MenuItem>
                    <MenuItem value="cdk">AWS CDK</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
            </Grid>

            <FormControl fullWidth sx={{ mb: 2 }}>
              <InputLabel>Environment</InputLabel>
              <Select
                value={request.environment}
                onChange={(e) => setRequest({ ...request, environment: e.target.value })}
              >
                <MenuItem value="development">Development</MenuItem>
                <MenuItem value="staging">Staging</MenuItem>
                <MenuItem value="production">Production</MenuItem>
              </Select>
            </FormControl>

            <Box mb={2}>
              <FormControlLabel
                control={
                  <Switch
                    checked={request.enable_validation}
                    onChange={(e) =>
                      setRequest({ ...request, enable_validation: e.target.checked })
                    }
                  />
                }
                label="Enable Validation"
              />
              <FormControlLabel
                control={
                  <Switch
                    checked={request.enable_optimization}
                    onChange={(e) =>
                      setRequest({ ...request, enable_optimization: e.target.checked })
                    }
                  />
                }
                label="Enable Optimization"
              />
            </Box>

            <Button
              variant="contained"
              fullWidth
              size="large"
              startIcon={generateMutation.isLoading ? <CircularProgress size={20} /> : <Code />}
              onClick={handleGenerate}
              disabled={
                !request.requirements.trim() ||
                !request.project_name.trim() ||
                generateMutation.isLoading
              }
              sx={{ mb: 2 }}
            >
              {generateMutation.isLoading ? 'Generating...' : 'Generate Code'}
            </Button>

            {generateMutation.isLoading && (
              <Box>
                <LinearProgress sx={{ mb: 1 }} />
                <Typography variant="body2" color="textSecondary" textAlign="center">
                  AI is generating your infrastructure code...
                </Typography>
              </Box>
            )}
          </Paper>

          {/* Examples */}
          {examples?.data && (
            <Paper sx={{ p: 3, mt: 2 }}>
              <Typography variant="h6" gutterBottom>
                Example Configurations
              </Typography>
              {Object.entries(examples.data.examples).map(([key, example]: [string, any]) => (
                <Card
                  key={key}
                  variant="outlined"
                  sx={{
                    mb: 1,
                    cursor: 'pointer',
                    '&:hover': { boxShadow: 2 },
                  }}
                  onClick={() => handleUseExample(example)}
                >
                  <CardContent sx={{ py: 1 }}>
                    <Typography variant="subtitle2" fontWeight="bold">
                      {example.description}
                    </Typography>
                    <Typography variant="caption" color="textSecondary">
                      {example.request.provider} • {example.request.format}
                    </Typography>
                  </CardContent>
                </Card>
              ))}
            </Paper>
          )}
        </Grid>

        {/* Results Panel */}
        <Grid item xs={12} md={8}>
          {generateMutation.error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              Failed to generate infrastructure code. Please try again.
            </Alert>
          )}

          {generationResult ? (
            <Paper sx={{ p: 0 }}>
              <Box sx={{ borderBottom: 1, borderColor: 'divider', px: 3, pt: 2 }}>
                <Box display="flex" justifyContent="between" alignItems="center" mb={2}>
                  <Tabs value={activeTab} onChange={(_, newValue) => setActiveTab(newValue)}>
                    <Tab icon={<Code />} label="Generated Code" />
                    <Tab icon={<Security />} label="Validation" />
                    <Tab icon={<TrendingUp />} label="Cost Estimate" />
                  </Tabs>

                  <Box display="flex" gap={1}>
                    <Button
                      size="small"
                      startIcon={<Build />}
                      onClick={handleValidate}
                      disabled={validateMutation.isLoading}
                    >
                      {validateMutation.isLoading ? 'Validating...' : 'Validate'}
                    </Button>
                    <Button
                      size="small"
                      startIcon={<Download />}
                      onClick={handleDownload}
                    >
                      Download
                    </Button>
                  </Box>
                </Box>
              </Box>

              <TabPanel value={activeTab} index={0}>
                <Box sx={{ height: 500 }}>
                  <Editor
                    height="100%"
                    defaultLanguage={request.format === 'terraform' ? 'hcl' : 'python'}
                    value={generationResult.infrastructure_code}
                    theme="vs-dark"
                    options={{
                      readOnly: false,
                      minimap: { enabled: false },
                      scrollBeyondLastLine: false,
                      fontSize: 14,
                      lineNumbers: 'on',
                      renderWhitespace: 'selection',
                      automaticLayout: true,
                    }}
                  />
                </Box>
              </TabPanel>

              <TabPanel value={activeTab} index={1}>
                <Box sx={{ px: 2 }}>
                  {validationResult ? (
                    renderValidationIssues(validationResult)
                  ) : (
                    <Alert severity="info">
                      <Box display="flex" alignItems="center" gap={1}>
                        <Visibility />
                        <Typography>Click "Validate" to check your infrastructure code</Typography>
                      </Box>
                    </Alert>
                  )}
                </Box>
              </TabPanel>

              <TabPanel value={activeTab} index={2}>
                <Box sx={{ px: 2 }}>
                  {generationResult.cost_estimate ? (
                    <Box>
                      <Typography variant="h6" mb={2}>
                        Estimated Monthly Cost: ${generationResult.cost_estimate.total_monthly_cost}
                      </Typography>
                      <List>
                        {generationResult.cost_estimate.breakdown.map((item, index) => (
                          <ListItem key={index} divider>
                            <ListItemText
                              primary={item.resource_name}
                              secondary={`${item.resource_type} - ${item.units || 1} units`}
                            />
                            <Typography variant="h6" color="primary">
                              ${item.monthly_cost}/month
                            </Typography>
                          </ListItem>
                        ))}
                      </List>
                      <Box display="flex" justifyContent="space-between" mt={2} p={2} bgcolor="action.hover" borderRadius={1}>
                        <Typography variant="h6">Total</Typography>
                        <Typography variant="h6" color="primary">
                          ${generationResult.cost_estimate.total_monthly_cost}/month
                        </Typography>
                      </Box>
                    </Box>
                  ) : (
                    <Alert severity="info">
                      Cost estimation not available for this configuration
                    </Alert>
                  )}
                </Box>
              </TabPanel>
            </Paper>
          ) : (
            <Paper sx={{ p: 4, textAlign: 'center', minHeight: 500 }}>
              <Code sx={{ fontSize: 80, color: 'text.secondary', mb: 2 }} />
              <Typography variant="h6" color="textSecondary" mb={1}>
                Ready to Generate
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Configure your requirements and click "Generate Code" to create infrastructure as code
              </Typography>
            </Paper>
          )}
        </Grid>
      </Grid>
    </Box>
  )
}
