import { useState } from 'react'
import { useQuery } from 'react-query'
import {
  Box,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Alert,
  LinearProgress,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material'
import {
  Security,
  Shield,
  Warning,
  Error,
  CheckCircle,
  ExpandMore,
  Scanner,
  Policy,
  Key,
  Lock,
  Refresh,
} from '@mui/icons-material'
import { securityApi } from '@/services/api'
import type { SecurityScanResult, SecurityFinding } from '@/types'

const mockSecurityData = {
  overallScore: 'A+',
  scoreValue: 98,
  lastScan: '2024-01-15T14:30:00Z',
  criticalFindings: 0,
  highFindings: 1,
  mediumFindings: 3,
  lowFindings: 5,
  infoFindings: 8,
}

const mockFindings: SecurityFinding[] = [
  {
    severity: 'high',
    type: 'configuration',
    title: 'Database passwords in plaintext',
    description: 'Database connection strings contain plaintext passwords in configuration files',
    file: 'config/database.yml',
    line: 15,
    remediation: 'Use environment variables or secure key management for database passwords',
  },
  {
    severity: 'medium',
    type: 'dependency',
    title: 'Outdated dependency with known vulnerabilities',
    description: 'Package "lodash" version 4.17.20 has known security vulnerabilities',
    file: 'package.json',
    line: 25,
    remediation: 'Update lodash to version 4.17.21 or later',
  },
  {
    severity: 'medium',
    type: 'network',
    title: 'Open SSH port on public interface',
    description: 'SSH port 22 is exposed on public network interface without IP restrictions',
    remediation: 'Restrict SSH access to specific IP ranges or use VPN',
  },
  {
    severity: 'low',
    type: 'compliance',
    title: 'Missing security headers',
    description: 'Web server missing recommended security headers (HSTS, CSP)',
    remediation: 'Configure security headers in web server configuration',
  },
]

const complianceChecks = [
  { name: 'GDPR Compliance', status: 'compliant', score: 95 },
  { name: 'SOC 2 Type II', status: 'compliant', score: 92 },
  { name: 'ISO 27001', status: 'partial', score: 78 },
  { name: 'PCI DSS', status: 'non-compliant', score: 45 },
  { name: 'HIPAA', status: 'not-applicable', score: null },
]

export default function SecurityCompliance() {
  const [selectedFinding, setSelectedFinding] = useState<SecurityFinding | null>(null)
  const [isDetailsDialogOpen, setIsDetailsDialogOpen] = useState(false)
  const [isScanning, setIsScanning] = useState(false)

  const { data: scanResults, refetch } = useQuery(
    'securityScan',
    () => securityApi.getStatus(),
    {
      refetchInterval: 30000,
      initialData: { data: mockSecurityData }
    }
  )

  const handleStartScan = async () => {
    setIsScanning(true)
    try {
      await securityApi.scan('comprehensive')
      await refetch()
    } catch (error) {
      console.error('Scan failed:', error)
    } finally {
      setIsScanning(false)
    }
  }

  const handleViewFinding = (finding: SecurityFinding) => {
    setSelectedFinding(finding)
    setIsDetailsDialogOpen(true)
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'error'
      case 'high': return 'error'
      case 'medium': return 'warning'
      case 'low': return 'info'
      case 'info': return 'default'
      default: return 'default'
    }
  }

  const getComplianceColor = (status: string) => {
    switch (status) {
      case 'compliant': return 'success'
      case 'partial': return 'warning'
      case 'non-compliant': return 'error'
      case 'not-applicable': return 'default'
      default: return 'default'
    }
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" gutterBottom fontWeight="bold">
            Security & Compliance
          </Typography>
          <Typography variant="body1" color="textSecondary">
            Monitor security posture and compliance status across your infrastructure
          </Typography>
        </Box>

        <Box display="flex" gap={2}>
          <Button variant="outlined" startIcon={<Refresh />} onClick={() => refetch()}>
            Refresh
          </Button>
          <Button
            variant="contained"
            startIcon={isScanning ? <LinearProgress size={20} /> : <Scanner />}
            onClick={handleStartScan}
            disabled={isScanning}
          >
            {isScanning ? 'Scanning...' : 'Run Security Scan'}
          </Button>
        </Box>
      </Box>

      {/* Security Overview */}
      <Grid container spacing={3} mb={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
              <Typography variant="h6">Security Score</Typography>
              <Shield color="success" sx={{ fontSize: 40 }} />
            </Box>
            <Box display="flex" alignItems="baseline" gap={1} mb={1}>
              <Typography variant="h2" fontWeight="bold" color="success.main">
                {mockSecurityData.overallScore}
              </Typography>
              <Typography variant="h6" color="textSecondary">
                ({mockSecurityData.scoreValue}/100)
              </Typography>
            </Box>
            <LinearProgress
              variant="determinate"
              value={mockSecurityData.scoreValue}
              sx={{ height: 8, borderRadius: 4, mb: 1 }}
            />
            <Typography variant="body2" color="textSecondary">
              Last scan: {new Date(mockSecurityData.lastScan).toLocaleString()}
            </Typography>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" mb={2}>Security Findings</Typography>
            <Grid container spacing={2}>
              <Grid item xs={6} sm={2.4}>
                <Box textAlign="center">
                  <Typography variant="h4" fontWeight="bold" color="error.main">
                    {mockSecurityData.criticalFindings}
                  </Typography>
                  <Typography variant="caption" color="textSecondary">
                    Critical
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={6} sm={2.4}>
                <Box textAlign="center">
                  <Typography variant="h4" fontWeight="bold" color="error.main">
                    {mockSecurityData.highFindings}
                  </Typography>
                  <Typography variant="caption" color="textSecondary">
                    High
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={6} sm={2.4}>
                <Box textAlign="center">
                  <Typography variant="h4" fontWeight="bold" color="warning.main">
                    {mockSecurityData.mediumFindings}
                  </Typography>
                  <Typography variant="caption" color="textSecondary">
                    Medium
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={6} sm={2.4}>
                <Box textAlign="center">
                  <Typography variant="h4" fontWeight="bold" color="info.main">
                    {mockSecurityData.lowFindings}
                  </Typography>
                  <Typography variant="caption" color="textSecondary">
                    Low
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={6} sm={2.4}>
                <Box textAlign="center">
                  <Typography variant="h4" fontWeight="bold" color="text.secondary">
                    {mockSecurityData.infoFindings}
                  </Typography>
                  <Typography variant="caption" color="textSecondary">
                    Info
                  </Typography>
                </Box>
              </Grid>
            </Grid>
          </Paper>
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        {/* Security Findings */}
        <Grid item xs={12} lg={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Security Findings
            </Typography>

            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Severity</TableCell>
                    <TableCell>Type</TableCell>
                    <TableCell>Title</TableCell>
                    <TableCell>File</TableCell>
                    <TableCell>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {mockFindings.map((finding, index) => (
                    <TableRow key={index} hover>
                      <TableCell>
                        <Chip
                          label={finding.severity.toUpperCase()}
                          size="small"
                          color={getSeverityColor(finding.severity) as any}
                        />
                      </TableCell>
                      <TableCell>
                        <Chip label={finding.type} size="small" variant="outlined" />
                      </TableCell>
                      <TableCell>
                        <Typography variant="subtitle2">
                          {finding.title}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        {finding.file && (
                          <Typography variant="body2" color="textSecondary">
                            {finding.file}
                            {finding.line && `:${finding.line}`}
                          </Typography>
                        )}
                      </TableCell>
                      <TableCell>
                        <Button
                          size="small"
                          onClick={() => handleViewFinding(finding)}
                        >
                          View
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </Grid>

        {/* Compliance Status */}
        <Grid item xs={12} lg={4}>
          <Paper sx={{ p: 3, mb: 2 }}>
            <Typography variant="h6" gutterBottom>
              Compliance Status
            </Typography>

            {complianceChecks.map((check, index) => (
              <Card key={index} variant="outlined" sx={{ mb: 1 }}>
                <CardContent sx={{ py: 1 }}>
                  <Box display="flex" justifyContent="space-between" alignItems="center">
                    <Typography variant="body2" fontWeight="medium">
                      {check.name}
                    </Typography>
                    <Box display="flex" alignItems="center" gap={1}>
                      {check.score && (
                        <Typography variant="caption" color="textSecondary">
                          {check.score}%
                        </Typography>
                      )}
                      <Chip
                        label={check.status.replace('-', ' ')}
                        size="small"
                        color={getComplianceColor(check.status) as any}
                      />
                    </Box>
                  </Box>
                  {check.score && (
                    <LinearProgress
                      variant="determinate"
                      value={check.score}
                      sx={{ mt: 1, height: 4, borderRadius: 2 }}
                      color={getComplianceColor(check.status) as any}
                    />
                  )}
                </CardContent>
              </Card>
            ))}
          </Paper>

          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Security Controls
            </Typography>

            <List dense>
              <ListItem>
                <ListItemIcon>
                  <CheckCircle color="success" />
                </ListItemIcon>
                <ListItemText primary="Pre-commit hooks" secondary="Active" />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <CheckCircle color="success" />
                </ListItemIcon>
                <ListItemText primary="Secret scanning" secondary="Active" />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <CheckCircle color="success" />
                </ListItemIcon>
                <ListItemText primary="Vulnerability scanning" secondary="Active" />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <Warning color="warning" />
                </ListItemIcon>
                <ListItemText primary="Runtime monitoring" secondary="Degraded" />
              </ListItem>
            </List>
          </Paper>
        </Grid>
      </Grid>

      {/* Finding Details Dialog */}
      <Dialog
        open={isDetailsDialogOpen}
        onClose={() => setIsDetailsDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          Security Finding Details
        </DialogTitle>
        <DialogContent>
          {selectedFinding && (
            <Box>
              <Box display="flex" gap={1} mb={2}>
                <Chip
                  label={selectedFinding.severity.toUpperCase()}
                  color={getSeverityColor(selectedFinding.severity) as any}
                />
                <Chip label={selectedFinding.type} variant="outlined" />
              </Box>

              <Typography variant="h6" mb={1}>
                {selectedFinding.title}
              </Typography>

              <Typography variant="body1" mb={2}>
                {selectedFinding.description}
              </Typography>

              {selectedFinding.file && (
                <Box mb={2}>
                  <Typography variant="subtitle2" fontWeight="bold">
                    File Location
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    {selectedFinding.file}
                    {selectedFinding.line && ` (Line ${selectedFinding.line})`}
                  </Typography>
                </Box>
              )}

              {selectedFinding.remediation && (
                <Box>
                  <Typography variant="subtitle2" fontWeight="bold" mb={1}>
                    Remediation
                  </Typography>
                  <Alert severity="info">
                    {selectedFinding.remediation}
                  </Alert>
                </Box>
              )}
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setIsDetailsDialogOpen(false)}>Close</Button>
          <Button variant="contained">Mark as Resolved</Button>
        </DialogActions>
      </Dialog>
    </Box>
  )
}
