import { useState } from 'react'
import { useQuery } from 'react-query'
import {
  Box,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  Chip,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Tabs,
  Tab,
} from '@mui/material'
import {
  PlayArrow,
  Stop,
  Refresh,
  Visibility,
  CheckCircle,
  Error,
  Warning,
  Schedule,
} from '@mui/icons-material'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { deploymentsApi } from '@/services/api'
import type { Deployment } from '@/types'

const mockDeployments: Deployment[] = [
  {
    id: '1',
    name: 'Web Server Cluster',
    status: 'running',
    provider: 'proxmox',
    environment: 'production',
    created_at: '2024-01-15T10:00:00Z',
    updated_at: '2024-01-15T14:30:00Z',
    requirements: 'Load-balanced web server cluster with 3 nodes',
  },
  {
    id: '2',
    name: 'Database Backup System',
    status: 'completed',
    provider: 'aws',
    environment: 'production',
    created_at: '2024-01-14T15:00:00Z',
    updated_at: '2024-01-14T16:00:00Z',
    requirements: 'Automated PostgreSQL backup with S3 storage',
  },
  {
    id: '3',
    name: 'Monitoring Stack',
    status: 'failed',
    provider: 'azure',
    environment: 'staging',
    created_at: '2024-01-13T09:00:00Z',
    updated_at: '2024-01-13T09:45:00Z',
    requirements: 'Prometheus, Grafana, and Loki monitoring setup',
  },
]

const mockMetricsData = [
  { time: '00:00', cpu: 45, memory: 62, disk: 78, network: 34 },
  { time: '04:00', cpu: 52, memory: 67, disk: 79, network: 41 },
  { time: '08:00', cpu: 78, memory: 72, disk: 80, network: 67 },
  { time: '12:00', cpu: 85, memory: 68, disk: 81, network: 73 },
  { time: '16:00', cpu: 71, memory: 74, disk: 82, network: 58 },
  { time: '20:00', cpu: 56, memory: 69, disk: 83, network: 45 },
]

export default function DeploymentMonitoring() {
  const [selectedDeployment, setSelectedDeployment] = useState<Deployment | null>(null)
  const [isDetailsDialogOpen, setIsDetailsDialogOpen] = useState(false)
  const [activeTab, setActiveTab] = useState(0)

  const { data: deployments, refetch } = useQuery(
    'deployments',
    () => deploymentsApi.list(),
    {
      initialData: { data: mockDeployments },
      refetchInterval: 30000 // Refresh every 30 seconds
    }
  )

  const handleViewDetails = (deployment: Deployment) => {
    setSelectedDeployment(deployment)
    setIsDetailsDialogOpen(true)
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running': return 'success'
      case 'completed': return 'info'
      case 'failed': return 'error'
      case 'pending': return 'warning'
      case 'stopped': return 'default'
      default: return 'default'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'running': return <PlayArrow color="success" />
      case 'completed': return <CheckCircle color="info" />
      case 'failed': return <Error color="error" />
      case 'pending': return <Schedule color="warning" />
      case 'stopped': return <Stop color="action" />
      default: return <Warning color="action" />
    }
  }

  const displayDeployments = deployments?.data || mockDeployments

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" gutterBottom fontWeight="bold">
            Deployment Monitoring
          </Typography>
          <Typography variant="body1" color="textSecondary">
            Monitor and manage active infrastructure deployments
          </Typography>
        </Box>

        <Button variant="outlined" startIcon={<Refresh />} onClick={() => refetch()}>
          Refresh
        </Button>
      </Box>

      {/* Status Overview */}
      <Grid container spacing={3} mb={3}>
        <Grid item xs={12} sm={3}>
          <Card>
            <CardContent sx={{ textAlign: 'center' }}>
              <Typography variant="h4" fontWeight="bold" color="success.main">
                {displayDeployments.filter(d => d.status === 'running').length}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Running
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={3}>
          <Card>
            <CardContent sx={{ textAlign: 'center' }}>
              <Typography variant="h4" fontWeight="bold" color="info.main">
                {displayDeployments.filter(d => d.status === 'completed').length}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Completed
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={3}>
          <Card>
            <CardContent sx={{ textAlign: 'center' }}>
              <Typography variant="h4" fontWeight="bold" color="error.main">
                {displayDeployments.filter(d => d.status === 'failed').length}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Failed
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={3}>
          <Card>
            <CardContent sx={{ textAlign: 'center' }}>
              <Typography variant="h4" fontWeight="bold" color="warning.main">
                {displayDeployments.filter(d => d.status === 'pending').length}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Pending
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Deployments Table */}
      <Paper>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Status</TableCell>
                <TableCell>Name</TableCell>
                <TableCell>Provider</TableCell>
                <TableCell>Environment</TableCell>
                <TableCell>Created</TableCell>
                <TableCell>Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {displayDeployments.map((deployment) => (
                <TableRow key={deployment.id} hover>
                  <TableCell>
                    <Box display="flex" alignItems="center" gap={1}>
                      {getStatusIcon(deployment.status)}
                      <Chip
                        label={deployment.status}
                        size="small"
                        color={getStatusColor(deployment.status) as any}
                      />
                    </Box>
                  </TableCell>
                  <TableCell>
                    <Typography variant="subtitle2" fontWeight="bold">
                      {deployment.name}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Chip label={deployment.provider} size="small" variant="outlined" />
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={deployment.environment}
                      size="small"
                      color={deployment.environment === 'production' ? 'error' : 'default'}
                    />
                  </TableCell>
                  <TableCell>
                    {new Date(deployment.created_at).toLocaleString()}
                  </TableCell>
                  <TableCell>
                    <IconButton
                      size="small"
                      onClick={() => handleViewDetails(deployment)}
                    >
                      <Visibility />
                    </IconButton>
                    {deployment.status === 'running' && (
                      <IconButton size="small" color="error">
                        <Stop />
                      </IconButton>
                    )}
                    {deployment.status === 'stopped' && (
                      <IconButton size="small" color="success">
                        <PlayArrow />
                      </IconButton>
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>

      {/* Deployment Details Dialog */}
      <Dialog
        open={isDetailsDialogOpen}
        onClose={() => setIsDetailsDialogOpen(false)}
        maxWidth="lg"
        fullWidth
      >
        <DialogTitle>
          {selectedDeployment?.name} - Details
        </DialogTitle>
        <DialogContent>
          {selectedDeployment && (
            <Box>
              <Tabs value={activeTab} onChange={(_, newValue) => setActiveTab(newValue)} sx={{ mb: 2 }}>
                <Tab label="Overview" />
                <Tab label="Metrics" />
                <Tab label="Logs" />
              </Tabs>

              {activeTab === 0 && (
                <Grid container spacing={2}>
                  <Grid item xs={12} md={6}>
                    <Typography variant="subtitle2" fontWeight="bold">Requirements</Typography>
                    <Typography variant="body2" mb={2}>{selectedDeployment.requirements}</Typography>

                    <Typography variant="subtitle2" fontWeight="bold">Provider</Typography>
                    <Typography variant="body2" mb={2}>{selectedDeployment.provider}</Typography>

                    <Typography variant="subtitle2" fontWeight="bold">Environment</Typography>
                    <Typography variant="body2" mb={2}>{selectedDeployment.environment}</Typography>
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <Typography variant="subtitle2" fontWeight="bold">Status</Typography>
                    <Chip
                      label={selectedDeployment.status}
                      color={getStatusColor(selectedDeployment.status) as any}
                      sx={{ mb: 2 }}
                    />

                    <Typography variant="subtitle2" fontWeight="bold">Created</Typography>
                    <Typography variant="body2" mb={2}>
                      {new Date(selectedDeployment.created_at).toLocaleString()}
                    </Typography>

                    <Typography variant="subtitle2" fontWeight="bold">Last Updated</Typography>
                    <Typography variant="body2">
                      {new Date(selectedDeployment.updated_at).toLocaleString()}
                    </Typography>
                  </Grid>
                </Grid>
              )}

              {activeTab === 1 && (
                <Box sx={{ height: 400 }}>
                  <Typography variant="h6" mb={2}>Resource Utilization</Typography>
                  <ResponsiveContainer width="100%" height="90%">
                    <LineChart data={mockMetricsData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="time" />
                      <YAxis />
                      <Tooltip />
                      <Line type="monotone" dataKey="cpu" stroke="#6366f1" name="CPU %" />
                      <Line type="monotone" dataKey="memory" stroke="#8b5cf6" name="Memory %" />
                      <Line type="monotone" dataKey="disk" stroke="#06b6d4" name="Disk %" />
                      <Line type="monotone" dataKey="network" stroke="#10b981" name="Network %" />
                    </LineChart>
                  </ResponsiveContainer>
                </Box>
              )}

              {activeTab === 2 && (
                <Box sx={{ height: 400, overflow: 'auto', bgcolor: '#1e1e1e', p: 2, borderRadius: 1 }}>
                  <Typography variant="body2" component="pre" sx={{ color: '#fff', fontFamily: 'monospace' }}>
{`[2024-01-15 14:30:15] INFO: Starting deployment process...
[2024-01-15 14:30:16] INFO: Validating infrastructure code...
[2024-01-15 14:30:18] INFO: Infrastructure code validation passed
[2024-01-15 14:30:19] INFO: Initializing Terraform...
[2024-01-15 14:30:25] INFO: Planning infrastructure changes...
[2024-01-15 14:30:30] INFO: Plan completed: 5 resources to add
[2024-01-15 14:30:31] INFO: Applying infrastructure changes...
[2024-01-15 14:32:45] INFO: proxmox_vm_qemu.web_server: Creating...
[2024-01-15 14:33:30] INFO: proxmox_vm_qemu.web_server: Creation complete
[2024-01-15 14:33:31] INFO: Deployment completed successfully`}
                  </Typography>
                </Box>
              )}
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setIsDetailsDialogOpen(false)}>Close</Button>
          {selectedDeployment?.status === 'running' && (
            <Button variant="outlined" color="error">Stop Deployment</Button>
          )}
          {selectedDeployment?.status === 'stopped' && (
            <Button variant="contained" color="success">Start Deployment</Button>
          )}
        </DialogActions>
      </Dialog>
    </Box>
  )
}
