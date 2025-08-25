import { useQuery } from 'react-query'
import {
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  LinearProgress,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  IconButton,
} from '@mui/material'
import {
  TrendingUp,
  Security,
  CloudQueue,
  Code,
  Warning,
  CheckCircle,
  Error,
  PlayArrow,
} from '@mui/icons-material'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import { healthApi, deploymentsApi, monitoringApi, workflowApi } from '@/services/api'

const COLORS = ['#6366f1', '#f59e0b', '#10b981', '#ef4444']

// Mock data for charts
const performanceData = [
  { name: '00:00', deployments: 12, success: 11, failed: 1 },
  { name: '04:00', deployments: 19, success: 18, failed: 1 },
  { name: '08:00', deployments: 25, success: 24, failed: 1 },
  { name: '12:00', deployments: 32, success: 30, failed: 2 },
  { name: '16:00', deployments: 28, success: 26, failed: 2 },
  { name: '20:00', deployments: 22, success: 21, failed: 1 },
]

const providerData = [
  { name: 'Proxmox', value: 45 },
  { name: 'AWS', value: 25 },
  { name: 'Azure', value: 20 },
  { name: 'GCP', value: 10 },
]

export default function Dashboard() {
  const { data: systemHealth } = useQuery('systemHealth', healthApi.getSystemHealth)
  const { data: deployments } = useQuery('deployments', () => deploymentsApi.list(1, 10))
  const { data: workflowItems } = useQuery('workflowItems', workflowApi.getWorkflowItems)

  const recentDeployments = Array.isArray(deployments?.data) ? deployments.data.slice(0, 5) : []
  const workflowStats = Array.isArray(workflowItems?.data) ? workflowItems.data.reduce((acc: any, item: any) => {
    acc[item.status] = (acc[item.status] || 0) + 1
    return acc
  }, {}) : {}

  return (
    <Box>
      <Typography variant="h4" gutterBottom fontWeight="bold">
        Dashboard Overview
      </Typography>

      {/* Key Metrics Cards */}
      <Grid container spacing={3} mb={3}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="textSecondary" gutterBottom variant="body2">
                    Active Deployments
                  </Typography>
                  <Typography variant="h5" fontWeight="bold">
                    24
                  </Typography>
                  <Box display="flex" alignItems="center" mt={1}>
                    <TrendingUp color="success" fontSize="small" />
                    <Typography variant="body2" color="success.main" ml={0.5}>
                      +12% from last week
                    </Typography>
                  </Box>
                </Box>
                <CloudQueue color="primary" sx={{ fontSize: 40 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="textSecondary" gutterBottom variant="body2">
                    Success Rate
                  </Typography>
                  <Typography variant="h5" fontWeight="bold">
                    94.2%
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={94.2}
                    sx={{ mt: 1, height: 6, borderRadius: 3 }}
                  />
                </Box>
                <CheckCircle color="success" sx={{ fontSize: 40 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="textSecondary" gutterBottom variant="body2">
                    Security Score
                  </Typography>
                  <Typography variant="h5" fontWeight="bold">
                    A+
                  </Typography>
                  <Typography variant="body2" color="success.main" mt={1}>
                    98/100 points
                  </Typography>
                </Box>
                <Security color="primary" sx={{ fontSize: 40 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="textSecondary" gutterBottom variant="body2">
                    Monthly Cost
                  </Typography>
                  <Typography variant="h5" fontWeight="bold">
                    $342
                  </Typography>
                  <Box display="flex" alignItems="center" mt={1}>
                    <TrendingUp color="success" fontSize="small" />
                    <Typography variant="body2" color="success.main" ml={0.5}>
                      -8% optimized
                    </Typography>
                  </Box>
                </Box>
                <TrendingUp color="primary" sx={{ fontSize: 40 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        {/* Performance Chart */}
        <Grid item xs={12} lg={8}>
          <Paper sx={{ p: 3, height: 400 }}>
            <Typography variant="h6" gutterBottom>
              Deployment Performance (Last 24h)
            </Typography>
            <ResponsiveContainer width="100%" height="90%">
              <LineChart data={performanceData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="deployments"
                  stroke="#6366f1"
                  strokeWidth={3}
                  name="Total Deployments"
                />
                <Line
                  type="monotone"
                  dataKey="success"
                  stroke="#10b981"
                  strokeWidth={2}
                  name="Successful"
                />
                <Line
                  type="monotone"
                  dataKey="failed"
                  stroke="#ef4444"
                  strokeWidth={2}
                  name="Failed"
                />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Provider Distribution */}
        <Grid item xs={12} lg={4}>
          <Paper sx={{ p: 3, height: 400 }}>
            <Typography variant="h6" gutterBottom>
              Provider Distribution
            </Typography>
            <ResponsiveContainer width="100%" height="90%">
              <PieChart>
                <Pie
                  data={providerData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {providerData.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Project Workflow Status */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Project Workflow Status
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={6}>
                <Box textAlign="center" p={2}>
                  <Typography variant="h4" fontWeight="bold" color="warning.main">
                    {workflowStats.Review || 0}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    In Review
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={6}>
                <Box textAlign="center" p={2}>
                  <Typography variant="h4" fontWeight="bold" color="primary.main">
                    {workflowStats.Ready || 0}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Ready
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={6}>
                <Box textAlign="center" p={2}>
                  <Typography variant="h4" fontWeight="bold" color="info.main">
                    {workflowStats['In Progress'] || 0}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    In Progress
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={6}>
                <Box textAlign="center" p={2}>
                  <Typography variant="h4" fontWeight="bold" color="success.main">
                    {workflowStats.Done || 0}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Done
                  </Typography>
                </Box>
              </Grid>
            </Grid>
          </Paper>
        </Grid>

        {/* Recent Deployments */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Recent Deployments
            </Typography>
            <List>
              {[
                { name: 'Web Server Cluster', status: 'running', provider: 'Proxmox' },
                { name: 'Database Backup', status: 'completed', provider: 'AWS' },
                { name: 'Load Balancer Setup', status: 'running', provider: 'Azure' },
                { name: 'Monitoring Stack', status: 'failed', provider: 'GCP' },
                { name: 'CI/CD Pipeline', status: 'pending', provider: 'Proxmox' },
              ].map((deployment, index) => (
                <ListItem key={index} divider>
                  <ListItemIcon>
                    {deployment.status === 'running' ? (
                      <PlayArrow color="primary" />
                    ) : deployment.status === 'completed' ? (
                      <CheckCircle color="success" />
                    ) : deployment.status === 'failed' ? (
                      <Error color="error" />
                    ) : (
                      <Warning color="warning" />
                    )}
                  </ListItemIcon>
                  <ListItemText
                    primary={deployment.name}
                    secondary={`Provider: ${deployment.provider}`}
                  />
                  <Chip
                    label={deployment.status}
                    size="small"
                    color={
                      deployment.status === 'running' ? 'primary' :
                      deployment.status === 'completed' ? 'success' :
                      deployment.status === 'failed' ? 'error' : 'warning'
                    }
                  />
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>

        {/* System Health */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              System Health & Services
            </Typography>
            <Grid container spacing={2}>
              {[
                { name: 'API Gateway', status: 'healthy', uptime: '99.9%' },
                { name: 'LLM Service', status: 'healthy', uptime: '99.7%' },
                { name: 'Database', status: 'healthy', uptime: '100%' },
                { name: 'Redis Cache', status: 'healthy', uptime: '99.8%' },
                { name: 'Temporal Workflows', status: 'degraded', uptime: '98.2%' },
                { name: 'Monitoring Stack', status: 'healthy', uptime: '99.9%' },
              ].map((service, index) => (
                <Grid item xs={12} sm={6} md={4} lg={2} key={index}>
                  <Card variant="outlined">
                    <CardContent sx={{ textAlign: 'center', py: 2 }}>
                      <Box
                        sx={{
                          width: 12,
                          height: 12,
                          borderRadius: '50%',
                          bgcolor: service.status === 'healthy' ? 'success.main' :
                                   service.status === 'degraded' ? 'warning.main' : 'error.main',
                          mx: 'auto',
                          mb: 1,
                        }}
                      />
                      <Typography variant="body2" fontWeight="medium">
                        {service.name}
                      </Typography>
                      <Typography variant="caption" color="textSecondary">
                        {service.uptime}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  )
}
