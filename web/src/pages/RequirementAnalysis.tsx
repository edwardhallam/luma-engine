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
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  CircularProgress,
  Alert,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  LinearProgress,
} from '@mui/material'
import {
  ExpandMore,
  Send,
  Psychology,
  Storage,
  Security,
  Cloud,
  Monitor,
  Router,
  Lightbulb,
  CheckCircle,
  Warning,
} from '@mui/icons-material'
import { requirementsApi } from '@/services/api'
import type { RequirementAnalysisRequest, RequirementAnalysisResponse } from '@/types'

const EXAMPLE_REQUIREMENTS = [
  {
    title: 'Simple Web Server',
    description: 'I need a simple web server running Ubuntu with nginx installed, accessible from the internet with basic security.',
  },
  {
    title: 'Database with High Availability',
    description: 'I need a PostgreSQL database server with 100GB storage, automated backups, and high availability setup for my production application.',
  },
  {
    title: 'Microservices Infrastructure',
    description: 'I need a microservices setup with load balancer, 3 application servers, Redis cache, monitoring stack, and CI/CD pipeline.',
  },
  {
    title: 'Development Environment',
    description: 'Create a development environment with GitLab, Jenkins CI/CD, artifact storage, and developer tools for a team of 5 developers.',
  },
]

export default function RequirementAnalysis() {
  const [requirements, setRequirements] = useState('')
  const [targetPlatform, setTargetPlatform] = useState('proxmox')
  const [environment, setEnvironment] = useState('development')
  const [analysisResult, setAnalysisResult] = useState<RequirementAnalysisResponse | null>(null)

  const { data: templates } = useQuery('requirementTemplates', () => requirementsApi.getTemplates())

  const analyzeMutation = useMutation(
    (request: RequirementAnalysisRequest) => requirementsApi.analyze(request),
    {
      onSuccess: (response) => {
        setAnalysisResult(response.data)
      },
    }
  )

  const handleAnalyze = () => {
    if (!requirements.trim()) return

    analyzeMutation.mutate({
      requirements,
      target_platform: targetPlatform,
      environment,
    })
  }

  const handleUseExample = (example: typeof EXAMPLE_REQUIREMENTS[0]) => {
    setRequirements(example.description)
  }

  const renderAnalysisSection = (title: string, items: any[], icon: React.ReactNode, color: string) => {
    if (!items || items.length === 0) return null

    return (
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMore />}>
          <Box display="flex" alignItems="center" gap={1}>
            {icon}
            <Typography variant="h6">{title}</Typography>
            <Chip label={items.length} size="small" sx={{ backgroundColor: color, color: 'white' }} />
          </Box>
        </AccordionSummary>
        <AccordionDetails>
          <List>
            {items.map((item, index) => (
              <ListItem key={index} divider>
                <ListItemIcon>
                  <CheckCircle color="success" />
                </ListItemIcon>
                <ListItemText
                  primary={item.name || item.type}
                  secondary={
                    <Box>
                      {item.specifications && (
                        <Box mt={1}>
                          {Object.entries(item.specifications).map(([key, value]) => (
                            <Chip
                              key={key}
                              label={`${key}: ${value}`}
                              size="small"
                              variant="outlined"
                              sx={{ mr: 0.5, mb: 0.5 }}
                            />
                          ))}
                        </Box>
                      )}
                      {item.configuration && (
                        <Box mt={1}>
                          {Object.entries(item.configuration).map(([key, value]) => (
                            <Chip
                              key={key}
                              label={`${key}: ${value}`}
                              size="small"
                              variant="outlined"
                              sx={{ mr: 0.5, mb: 0.5 }}
                            />
                          ))}
                        </Box>
                      )}
                    </Box>
                  }
                />
              </ListItem>
            ))}
          </List>
        </AccordionDetails>
      </Accordion>
    )
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom fontWeight="bold">
        Requirements Analysis
      </Typography>
      <Typography variant="body1" color="textSecondary" mb={3}>
        Describe your infrastructure needs in natural language and get AI-powered analysis
      </Typography>

      <Grid container spacing={3}>
        {/* Input Section */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Describe Your Requirements
            </Typography>

            <TextField
              fullWidth
              multiline
              rows={8}
              placeholder="Describe what you need... For example: 'I need a web server with a database, load balancer, and monitoring for a small e-commerce site that can handle 1000 users.'"
              value={requirements}
              onChange={(e) => setRequirements(e.target.value)}
              sx={{ mb: 2 }}
            />

            <Grid container spacing={2} mb={2}>
              <Grid item xs={6}>
                <FormControl fullWidth>
                  <InputLabel>Target Platform</InputLabel>
                  <Select
                    value={targetPlatform}
                    onChange={(e) => setTargetPlatform(e.target.value)}
                  >
                    <MenuItem value="proxmox">Proxmox</MenuItem>
                    <MenuItem value="aws">AWS</MenuItem>
                    <MenuItem value="azure">Azure</MenuItem>
                    <MenuItem value="gcp">Google Cloud</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={6}>
                <FormControl fullWidth>
                  <InputLabel>Environment</InputLabel>
                  <Select
                    value={environment}
                    onChange={(e) => setEnvironment(e.target.value)}
                  >
                    <MenuItem value="development">Development</MenuItem>
                    <MenuItem value="staging">Staging</MenuItem>
                    <MenuItem value="production">Production</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
            </Grid>

            <Button
              variant="contained"
              fullWidth
              size="large"
              startIcon={analyzeMutation.isLoading ? <CircularProgress size={20} /> : <Psychology />}
              onClick={handleAnalyze}
              disabled={!requirements.trim() || analyzeMutation.isLoading}
            >
              {analyzeMutation.isLoading ? 'Analyzing...' : 'Analyze Requirements'}
            </Button>

            {analyzeMutation.isLoading && (
              <Box mt={2}>
                <LinearProgress />
                <Typography variant="body2" color="textSecondary" mt={1} textAlign="center">
                  AI agents are analyzing your requirements...
                </Typography>
              </Box>
            )}
          </Paper>

          {/* Example Requirements */}
          <Paper sx={{ p: 3, mt: 2 }}>
            <Typography variant="h6" gutterBottom>
              Example Requirements
            </Typography>
            <Grid container spacing={2}>
              {EXAMPLE_REQUIREMENTS.map((example, index) => (
                <Grid item xs={12} sm={6} key={index}>
                  <Card
                    variant="outlined"
                    sx={{
                      cursor: 'pointer',
                      '&:hover': { boxShadow: 2 },
                      transition: 'box-shadow 0.2s',
                    }}
                    onClick={() => handleUseExample(example)}
                  >
                    <CardContent>
                      <Typography variant="subtitle2" fontWeight="bold" mb={1}>
                        {example.title}
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        {example.description}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </Paper>
        </Grid>

        {/* Results Section */}
        <Grid item xs={12} md={6}>
          {analyzeMutation.error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              Failed to analyze requirements. Please try again.
            </Alert>
          )}

          {analysisResult ? (
            <Paper sx={{ p: 3 }}>
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                <Typography variant="h6">
                  Analysis Results
                </Typography>
                <Box display="flex" gap={1}>
                  <Chip
                    label={`${Math.round(analysisResult.confidence_score * 100)}% confidence`}
                    color="success"
                    size="small"
                  />
                  <Chip
                    label={`${analysisResult.processing_time.toFixed(2)}s`}
                    variant="outlined"
                    size="small"
                  />
                </Box>
              </Box>

              <Box mb={3}>
                {renderAnalysisSection(
                  'Infrastructure Components',
                  analysisResult.analysis.infrastructure_components,
                  <Cloud />,
                  '#6366f1'
                )}

                {renderAnalysisSection(
                  'Compute Requirements',
                  analysisResult.analysis.compute_requirements,
                  <Psychology />,
                  '#8b5cf6'
                )}

                {renderAnalysisSection(
                  'Storage Requirements',
                  analysisResult.analysis.storage_requirements,
                  <Storage />,
                  '#06b6d4'
                )}

                {renderAnalysisSection(
                  'Networking Requirements',
                  analysisResult.analysis.networking_requirements,
                  <Router />,
                  '#10b981'
                )}

                {renderAnalysisSection(
                  'Security Requirements',
                  analysisResult.analysis.security_requirements,
                  <Security />,
                  '#f59e0b'
                )}

                {renderAnalysisSection(
                  'Monitoring Requirements',
                  analysisResult.analysis.monitoring_requirements,
                  <Monitor />,
                  '#ef4444'
                )}
              </Box>

              {analysisResult.suggestions && analysisResult.suggestions.length > 0 && (
                <Box>
                  <Typography variant="h6" mb={1} display="flex" alignItems="center" gap={1}>
                    <Lightbulb color="warning" />
                    AI Suggestions
                  </Typography>
                  <List>
                    {analysisResult.suggestions.map((suggestion, index) => (
                      <ListItem key={index}>
                        <ListItemIcon>
                          <Warning color="warning" />
                        </ListItemIcon>
                        <ListItemText primary={suggestion} />
                      </ListItem>
                    ))}
                  </List>
                </Box>
              )}

              <Box mt={3}>
                <Button
                  variant="contained"
                  fullWidth
                  startIcon={<Send />}
                >
                  Generate Infrastructure Code
                </Button>
              </Box>
            </Paper>
          ) : (
            <Paper sx={{ p: 3, textAlign: 'center' }}>
              <Psychology sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
              <Typography variant="h6" color="textSecondary" mb={1}>
                Ready to Analyze
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Enter your requirements and click "Analyze" to get AI-powered infrastructure recommendations
              </Typography>
            </Paper>
          )}
        </Grid>
      </Grid>
    </Box>
  )
}
