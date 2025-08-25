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
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Switch,
  FormControlLabel,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
} from '@mui/material'
import {
  TrendingUp,
  TrendingDown,
  Warning,
  CheckCircle,
  Savings,
  CloudQueue,
  Storage,
  Memory,
  Lightbulb,
} from '@mui/icons-material'
import { PieChart, Pie, Cell, ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, BarChart, Bar } from 'recharts'

const COLORS = ['#6366f1', '#8b5cf6', '#06b6d4', '#10b981', '#f59e0b', '#ef4444']

const mockCostData = {
  totalMonthlyCost: 1247.89,
  lastMonthCost: 1356.42,
  potentialSavings: 312.56,
  optimizationScore: 78,
}

const mockResourceCosts = [
  { name: 'Compute (EC2)', value: 567.34, percentage: 45.5, trend: 'up' },
  { name: 'Storage (S3)', value: 234.12, percentage: 18.8, trend: 'down' },
  { name: 'Networking', value: 187.90, percentage: 15.1, trend: 'stable' },
  { name: 'Database (RDS)', value: 156.78, percentage: 12.6, trend: 'up' },
  { name: 'Load Balancers', value: 67.45, percentage: 5.4, trend: 'stable' },
  { name: 'Other Services', value: 34.30, percentage: 2.6, trend: 'down' },
]

const mockTrendData = [
  { month: 'Jul', cost: 1189.23, optimized: 1087.45 },
  { month: 'Aug', cost: 1245.67, optimized: 1123.78 },
  { month: 'Sep', cost: 1298.34, optimized: 1167.23 },
  { month: 'Oct', cost: 1356.42, optimized: 1198.90 },
  { month: 'Nov', cost: 1247.89, optimized: 1156.34 },
  { month: 'Dec', cost: 1289.45, optimized: 1167.89 },
]

const mockOptimizations = [
  {
    id: '1',
    type: 'rightsizing',
    title: 'Downsize over-provisioned EC2 instances',
    description: 'Instance i-0123456789abcdef0 (t3.large) has consistently low CPU utilization',
    potentialSavings: 89.50,
    impact: 'medium',
    effort: 'low',
    status: 'recommended',
  },
  {
    id: '2',
    type: 'storage',
    title: 'Move infrequently accessed S3 objects to IA',
    description: 'Objects in bucket "backups" haven\'t been accessed in 60+ days',
    potentialSavings: 123.45,
    impact: 'high',
    effort: 'low',
    status: 'recommended',
  },
  {
    id: '3',
    type: 'scheduling',
    title: 'Schedule dev environment shutdown',
    description: 'Development instances running 24/7 when only needed during business hours',
    potentialSavings: 156.78,
    impact: 'high',
    effort: 'medium',
    status: 'in_progress',
  },
  {
    id: '4',
    type: 'commitment',
    title: 'Purchase Reserved Instances',
    description: 'Long-running production instances eligible for Reserved Instance pricing',
    potentialSavings: 234.56,
    impact: 'high',
    effort: 'high',
    status: 'recommended',
  },
]

export default function CostOptimization() {
  const [selectedTimeRange, setSelectedTimeRange] = useState('6m')
  const [autoOptimization, setAutoOptimization] = useState(false)
  const [selectedOptimization, setSelectedOptimization] = useState(null)
  const [isDetailsDialogOpen, setIsDetailsDialogOpen] = useState(false)

  const getImpactColor = (impact: string) => {
    switch (impact) {
      case 'high': return 'success'
      case 'medium': return 'warning'
      case 'low': return 'info'
      default: return 'default'
    }
  }

  const getEffortColor = (effort: string) => {
    switch (effort) {
      case 'low': return 'success'
      case 'medium': return 'warning'
      case 'high': return 'error'
      default: return 'default'
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'recommended': return 'info'
      case 'in_progress': return 'warning'
      case 'completed': return 'success'
      case 'dismissed': return 'default'
      default: return 'default'
    }
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" gutterBottom fontWeight="bold">
            Cost Optimization
          </Typography>
          <Typography variant="body1" color="textSecondary">
            Monitor costs and discover optimization opportunities across your infrastructure
          </Typography>
        </Box>

        <Box display="flex" alignItems="center" gap={2}>
          <FormControlLabel
            control={
              <Switch
                checked={autoOptimization}
                onChange={(e) => setAutoOptimization(e.target.checked)}
              />
            }
            label="Auto-optimization"
          />
          <FormControl size="small" sx={{ minWidth: 120 }}>
            <InputLabel>Time Range</InputLabel>
            <Select
              value={selectedTimeRange}
              onChange={(e) => setSelectedTimeRange(e.target.value)}
            >
              <MenuItem value="1m">1 Month</MenuItem>
              <MenuItem value="3m">3 Months</MenuItem>
              <MenuItem value="6m">6 Months</MenuItem>
              <MenuItem value="1y">1 Year</MenuItem>
            </Select>
          </FormControl>
        </Box>
      </Box>

      {/* Cost Overview */}
      <Grid container spacing={3} mb={3}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="textSecondary" gutterBottom variant="body2">
                    Monthly Cost
                  </Typography>
                  <Typography variant="h5" fontWeight="bold">
                    ${mockCostData.totalMonthlyCost.toLocaleString()}
                  </Typography>
                  <Box display="flex" alignItems="center" mt={1}>
                    <TrendingDown color="success" fontSize="small" />
                    <Typography variant="body2" color="success.main" ml={0.5}>
                      -8.0% vs last month
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
                    Potential Savings
                  </Typography>
                  <Typography variant="h5" fontWeight="bold" color="success.main">
                    ${mockCostData.potentialSavings.toLocaleString()}
                  </Typography>
                  <Typography variant="body2" color="textSecondary" mt={1}>
                    25% of current spend
                  </Typography>
                </Box>
                <Savings color="success" sx={{ fontSize: 40 }} />
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
                    Optimization Score
                  </Typography>
                  <Typography variant="h5" fontWeight="bold" color="warning.main">
                    {mockCostData.optimizationScore}%
                  </Typography>
                  <Typography variant="body2" color="textSecondary" mt={1}>
                    Good, room for improvement
                  </Typography>
                </Box>
                <TrendingUp color="warning" sx={{ fontSize: 40 }} />
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
                    Active Optimizations
                  </Typography>
                  <Typography variant="h5" fontWeight="bold">
                    {mockOptimizations.filter(o => o.status === 'in_progress').length}
                  </Typography>
                  <Typography variant="body2" color="textSecondary" mt={1}>
                    In progress
                  </Typography>
                </Box>
                <Lightbulb color="info" sx={{ fontSize: 40 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        {/* Cost Breakdown */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, height: 400 }}>
            <Typography variant="h6" gutterBottom>
              Cost Breakdown by Service
            </Typography>
            <ResponsiveContainer width="100%" height="85%">
              <PieChart>
                <Pie
                  data={mockResourceCosts}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percentage }) => `${name} (${percentage.toFixed(1)}%)`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {mockResourceCosts.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={(value) => [`$${value}`, 'Cost']} />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Cost Trends */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, height: 400 }}>
            <Typography variant="h6" gutterBottom>
              Cost Trends
            </Typography>
            <ResponsiveContainer width="100%" height="85%">
              <LineChart data={mockTrendData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip formatter={(value) => [`$${value}`, '']} />
                <Line
                  type="monotone"
                  dataKey="cost"
                  stroke="#ef4444"
                  strokeWidth={3}
                  name="Actual Cost"
                />
                <Line
                  type="monotone"
                  dataKey="optimized"
                  stroke="#10b981"
                  strokeWidth={2}
                  strokeDasharray="5 5"
                  name="Optimized Cost"
                />
              </LineChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Resource Usage */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Optimization Recommendations
            </Typography>

            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Optimization</TableCell>
                    <TableCell>Potential Savings</TableCell>
                    <TableCell>Impact</TableCell>
                    <TableCell>Effort</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {mockOptimizations.map((optimization) => (
                    <TableRow key={optimization.id} hover>
                      <TableCell>
                        <Typography variant="subtitle2" fontWeight="bold">
                          {optimization.title}
                        </Typography>
                        <Typography variant="body2" color="textSecondary" sx={{
                          maxWidth: 300,
                          overflow: 'hidden',
                          textOverflow: 'ellipsis',
                        }}>
                          {optimization.description}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Typography variant="h6" color="success.main" fontWeight="bold">
                          ${optimization.potentialSavings}/mo
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={optimization.impact}
                          size="small"
                          color={getImpactColor(optimization.impact) as any}
                        />
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={optimization.effort}
                          size="small"
                          color={getEffortColor(optimization.effort) as any}
                          variant="outlined"
                        />
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={optimization.status.replace('_', ' ')}
                          size="small"
                          color={getStatusColor(optimization.status) as any}
                        />
                      </TableCell>
                      <TableCell>
                        <Button size="small" variant="outlined">
                          {optimization.status === 'recommended' ? 'Apply' : 'View'}
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </Grid>

        {/* Quick Actions */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, mb: 2 }}>
            <Typography variant="h6" gutterBottom>
              Quick Actions
            </Typography>

            <List>
              <ListItem>
                <ListItemIcon>
                  <CheckCircle color="success" />
                </ListItemIcon>
                <ListItemText
                  primary="Enable cost alerts"
                  secondary="Get notified when costs exceed thresholds"
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <Warning color="warning" />
                </ListItemIcon>
                <ListItemText
                  primary="Review unused resources"
                  secondary="14 resources haven't been used in 30 days"
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <Lightbulb color="info" />
                </ListItemIcon>
                <ListItemText
                  primary="Optimize storage classes"
                  secondary="Move old data to cheaper storage tiers"
                />
              </ListItem>
            </List>
          </Paper>

          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Savings This Month
            </Typography>

            <Alert severity="success" sx={{ mb: 2 }}>
              You've saved $108.53 this month through optimization!
            </Alert>

            <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
              <Typography variant="body2">Progress to goal</Typography>
              <Typography variant="body2" color="textSecondary">
                $108 / $200
              </Typography>
            </Box>
            <Box sx={{ height: 8, bgcolor: 'grey.200', borderRadius: 4, mb: 2 }}>
              <Box
                sx={{
                  height: '100%',
                  bgcolor: 'success.main',
                  borderRadius: 4,
                  width: '54%',
                }}
              />
            </Box>

            <Typography variant="caption" color="textSecondary">
              54% of monthly savings goal achieved
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  )
}
