import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from 'react-query'
import {
  Box,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  Chip,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Fab,
  IconButton,
  Menu,
  MenuItem,
  Tabs,
  Tab,
} from '@mui/material'
import {
  Add,
  MoreVert,
  Edit,
  Delete,
  Visibility,
  Code,
  Cloud,
  Storage,
} from '@mui/icons-material'
import Editor from '@monaco-editor/react'
import { templatesApi } from '@/services/api'
import type { Template } from '@/types'

const CATEGORIES = ['Web Services', 'Databases', 'Networking', 'Security', 'Monitoring', 'Storage']
const PROVIDERS = ['proxmox', 'aws', 'azure', 'gcp', 'digitalocean']

export default function TemplateManagement() {
  const [selectedCategory, setSelectedCategory] = useState('')
  const [selectedProvider, setSelectedProvider] = useState('')
  const [selectedTemplate, setSelectedTemplate] = useState<Template | null>(null)
  const [isViewDialogOpen, setIsViewDialogOpen] = useState(false)
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false)
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null)
  const [activeTab, setActiveTab] = useState(0)

  const queryClient = useQueryClient()

  const { data: templates, isLoading } = useQuery(
    ['templates', selectedCategory, selectedProvider],
    () => templatesApi.list(selectedCategory, selectedProvider)
  )

  const deleteMutation = useMutation(
    (id: string) => templatesApi.delete(id),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('templates')
      },
    }
  )

  const handleViewTemplate = (template: Template) => {
    setSelectedTemplate(template)
    setIsViewDialogOpen(true)
  }

  const handleEditTemplate = (template: Template) => {
    setSelectedTemplate(template)
    setIsEditDialogOpen(true)
    setAnchorEl(null)
  }

  const handleDeleteTemplate = (id: string) => {
    if (window.confirm('Are you sure you want to delete this template?')) {
      deleteMutation.mutate(id)
    }
    setAnchorEl(null)
  }

  const mockTemplates: Template[] = [
    {
      id: '1',
      name: 'Ubuntu Web Server',
      description: 'Basic Ubuntu server with nginx and SSL certificates',
      category: 'Web Services',
      provider: 'proxmox',
      template_content: `resource "proxmox_vm_qemu" "web_server" {
  name        = var.vm_name
  target_node = var.proxmox_node
  clone       = var.template_name

  memory = var.memory
  cores  = var.cores

  disk {
    size    = var.disk_size
    type    = "scsi"
    storage = var.storage
  }

  network {
    model  = "virtio"
    bridge = var.network_bridge
  }
}`,
      variables: [
        { name: 'vm_name', type: 'string', description: 'Name of the VM', required: true },
        { name: 'memory', type: 'number', description: 'Memory in MB', default_value: 2048, required: true },
        { name: 'cores', type: 'number', description: 'Number of CPU cores', default_value: 2, required: true },
      ],
      created_at: '2024-01-15T10:00:00Z',
      updated_at: '2024-01-15T10:00:00Z',
    },
    {
      id: '2',
      name: 'PostgreSQL Database',
      description: 'PostgreSQL database with automated backups',
      category: 'Databases',
      provider: 'aws',
      template_content: `resource "aws_db_instance" "postgres" {
  identifier = var.db_identifier
  engine     = "postgres"

  allocated_storage = var.allocated_storage
  instance_class    = var.instance_class

  db_name  = var.database_name
  username = var.username
  password = var.password

  backup_retention_period = var.backup_retention
  backup_window          = var.backup_window
}`,
      variables: [
        { name: 'db_identifier', type: 'string', description: 'Database identifier', required: true },
        { name: 'allocated_storage', type: 'number', description: 'Storage size in GB', default_value: 100, required: true },
        { name: 'instance_class', type: 'string', description: 'Instance class', default_value: 'db.t3.micro', required: true },
      ],
      created_at: '2024-01-14T15:30:00Z',
      updated_at: '2024-01-14T15:30:00Z',
    },
  ]

  const displayTemplates = templates?.data || mockTemplates

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" gutterBottom fontWeight="bold">
            Template Management
          </Typography>
          <Typography variant="body1" color="textSecondary">
            Manage reusable infrastructure templates and patterns
          </Typography>
        </Box>

        <Fab color="primary" onClick={() => setIsEditDialogOpen(true)}>
          <Add />
        </Fab>
      </Box>

      {/* Filters */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} md={4}>
            <TextField
              fullWidth
              select
              label="Category"
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
            >
              <MenuItem value="">All Categories</MenuItem>
              {CATEGORIES.map((category) => (
                <MenuItem key={category} value={category}>
                  {category}
                </MenuItem>
              ))}
            </TextField>
          </Grid>
          <Grid item xs={12} md={4}>
            <TextField
              fullWidth
              select
              label="Provider"
              value={selectedProvider}
              onChange={(e) => setSelectedProvider(e.target.value)}
            >
              <MenuItem value="">All Providers</MenuItem>
              {PROVIDERS.map((provider) => (
                <MenuItem key={provider} value={provider}>
                  {provider.charAt(0).toUpperCase() + provider.slice(1)}
                </MenuItem>
              ))}
            </TextField>
          </Grid>
          <Grid item xs={12} md={4}>
            <Typography variant="body2" color="textSecondary">
              {displayTemplates.length} templates found
            </Typography>
          </Grid>
        </Grid>
      </Paper>

      {/* Templates Grid */}
      <Grid container spacing={3}>
        {displayTemplates.map((template) => (
          <Grid item xs={12} sm={6} md={4} key={template.id}>
            <Card>
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={2}>
                  <Typography variant="h6" fontWeight="bold">
                    {template.name}
                  </Typography>
                  <IconButton
                    size="small"
                    onClick={(e) => {
                      setAnchorEl(e.currentTarget)
                      setSelectedTemplate(template)
                    }}
                  >
                    <MoreVert />
                  </IconButton>
                </Box>

                <Typography variant="body2" color="textSecondary" mb={2} sx={{
                  display: '-webkit-box',
                  overflow: 'hidden',
                  WebkitBoxOrient: 'vertical',
                  WebkitLineClamp: 2,
                }}>
                  {template.description}
                </Typography>

                <Box display="flex" gap={1} mb={2} flexWrap="wrap">
                  <Chip
                    icon={<Cloud />}
                    label={template.provider}
                    size="small"
                    color="primary"
                  />
                  <Chip
                    icon={<Code />}
                    label={template.category}
                    size="small"
                    variant="outlined"
                  />
                  <Chip
                    label={`${template.variables.length} vars`}
                    size="small"
                    variant="outlined"
                  />
                </Box>

                <Typography variant="caption" color="textSecondary">
                  Updated {new Date(template.updated_at).toLocaleDateString()}
                </Typography>
              </CardContent>

              <CardActions>
                <Button
                  size="small"
                  startIcon={<Visibility />}
                  onClick={() => handleViewTemplate(template)}
                >
                  View
                </Button>
                <Button
                  size="small"
                  startIcon={<Edit />}
                  onClick={() => handleEditTemplate(template)}
                >
                  Edit
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Context Menu */}
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={() => setAnchorEl(null)}
      >
        <MenuItem onClick={() => selectedTemplate && handleEditTemplate(selectedTemplate)}>
          <Edit sx={{ mr: 1 }} fontSize="small" />
          Edit
        </MenuItem>
        <MenuItem onClick={() => selectedTemplate && handleDeleteTemplate(selectedTemplate.id)}>
          <Delete sx={{ mr: 1 }} fontSize="small" />
          Delete
        </MenuItem>
      </Menu>

      {/* View Template Dialog */}
      <Dialog
        open={isViewDialogOpen}
        onClose={() => setIsViewDialogOpen(false)}
        maxWidth="lg"
        fullWidth
      >
        <DialogTitle>{selectedTemplate?.name}</DialogTitle>
        <DialogContent>
          {selectedTemplate && (
            <Box>
              <Tabs value={activeTab} onChange={(_, newValue) => setActiveTab(newValue)} sx={{ mb: 2 }}>
                <Tab label="Template Code" />
                <Tab label="Variables" />
                <Tab label="Details" />
              </Tabs>

              {activeTab === 0 && (
                <Box sx={{ height: 400 }}>
                  <Editor
                    height="100%"
                    defaultLanguage="hcl"
                    value={selectedTemplate.template_content}
                    theme="vs-dark"
                    options={{
                      readOnly: true,
                      minimap: { enabled: false },
                    }}
                  />
                </Box>
              )}

              {activeTab === 1 && (
                <Box>
                  {selectedTemplate.variables.map((variable, index) => (
                    <Card key={index} variant="outlined" sx={{ mb: 1 }}>
                      <CardContent sx={{ py: 1 }}>
                        <Typography variant="subtitle2" fontWeight="bold">
                          {variable.name} ({variable.type})
                        </Typography>
                        <Typography variant="body2" color="textSecondary">
                          {variable.description}
                        </Typography>
                        {variable.default_value && (
                          <Typography variant="caption">
                            Default: {variable.default_value}
                          </Typography>
                        )}
                        {variable.required && (
                          <Chip label="Required" size="small" color="error" sx={{ ml: 1 }} />
                        )}
                      </CardContent>
                    </Card>
                  ))}
                </Box>
              )}

              {activeTab === 2 && (
                <Box>
                  <Typography><strong>Category:</strong> {selectedTemplate.category}</Typography>
                  <Typography><strong>Provider:</strong> {selectedTemplate.provider}</Typography>
                  <Typography><strong>Created:</strong> {new Date(selectedTemplate.created_at).toLocaleString()}</Typography>
                  <Typography><strong>Updated:</strong> {new Date(selectedTemplate.updated_at).toLocaleString()}</Typography>
                </Box>
              )}
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setIsViewDialogOpen(false)}>Close</Button>
          <Button variant="contained" onClick={() => selectedTemplate && handleEditTemplate(selectedTemplate)}>
            Edit Template
          </Button>
        </DialogActions>
      </Dialog>

      {/* Edit/Create Template Dialog */}
      <Dialog
        open={isEditDialogOpen}
        onClose={() => setIsEditDialogOpen(false)}
        maxWidth="lg"
        fullWidth
      >
        <DialogTitle>
          {selectedTemplate ? 'Edit Template' : 'Create New Template'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 2 }}>
            <Grid container spacing={2} mb={2}>
              <Grid item xs={6}>
                <TextField
                  fullWidth
                  label="Template Name"
                  value={selectedTemplate?.name || ''}
                />
              </Grid>
              <Grid item xs={6}>
                <TextField
                  fullWidth
                  select
                  label="Category"
                  value={selectedTemplate?.category || ''}
                >
                  {CATEGORIES.map((category) => (
                    <MenuItem key={category} value={category}>
                      {category}
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
            </Grid>

            <TextField
              fullWidth
              multiline
              rows={2}
              label="Description"
              value={selectedTemplate?.description || ''}
              sx={{ mb: 2 }}
            />

            <Box sx={{ height: 400, mb: 2 }}>
              <Editor
                height="100%"
                defaultLanguage="hcl"
                value={selectedTemplate?.template_content || ''}
                theme="vs-dark"
                options={{
                  minimap: { enabled: false },
                }}
              />
            </Box>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setIsEditDialogOpen(false)}>Cancel</Button>
          <Button variant="contained">
            {selectedTemplate ? 'Update' : 'Create'} Template
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  )
}
