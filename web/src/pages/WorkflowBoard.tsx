import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from 'react-query'
import {
  Box,
  Typography,
  Paper,
  Card,
  CardContent,
  Chip,
  Avatar,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Grid,
} from '@mui/material'
import {
  MoreVert,
  Edit,
  Add,
  GitHub,
} from '@mui/icons-material'
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd'
import { workflowApi } from '@/services/api'
import type { WorkflowItem } from '@/types'

const COLUMN_ORDER = ['Review', 'Ready', 'In Progress', 'Done']
const PRIORITY_COLORS = {
  High: '#ef4444',
  Medium: '#f59e0b',
  Low: '#10b981',
}

const SIZE_COLORS = {
  Large: '#6366f1',
  Medium: '#8b5cf6',
  Small: '#06b6d4',
}

export default function WorkflowBoard() {
  const [selectedItem, setSelectedItem] = useState<WorkflowItem | null>(null)
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false)
  const queryClient = useQueryClient()

  const { data: workflowItems, isLoading } = useQuery('workflowItems', workflowApi.getWorkflowItems)

  const updateItemMutation = useMutation(
    ({ id, updates }: { id: string; updates: Partial<WorkflowItem> }) =>
      workflowApi.updateWorkflowItem(id, updates),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('workflowItems')
      },
    }
  )

  const handleDragEnd = (result: any) => {
    if (!result.destination) return

    const { draggableId, destination } = result
    const newStatus = destination.droppableId as WorkflowItem['status']

    updateItemMutation.mutate({
      id: draggableId,
      updates: { status: newStatus },
    })
  }

  const handleEditItem = (item: WorkflowItem) => {
    setSelectedItem(item)
    setIsEditDialogOpen(true)
  }

  const handleUpdateItem = () => {
    if (!selectedItem) return

    updateItemMutation.mutate({
      id: selectedItem.id,
      updates: selectedItem,
    })
    setIsEditDialogOpen(false)
    setSelectedItem(null)
  }

  const items = workflowItems?.data || []
  const itemsByStatus = COLUMN_ORDER.reduce((acc, status) => {
    acc[status] = items.filter((item: WorkflowItem) => item.status === status)
    return acc
  }, {} as Record<string, WorkflowItem[]>)

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="50vh">
        <Typography>Loading workflow...</Typography>
      </Box>
    )
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Box>
          <Typography variant="h4" gutterBottom fontWeight="bold">
            Project Workflow Board
          </Typography>
          <Typography variant="body1" color="textSecondary">
            Track and manage LumaEngine development tasks across the project lifecycle
          </Typography>
        </Box>

        <Box display="flex" gap={2}>
          <Button
            variant="outlined"
            startIcon={<GitHub />}
            href="https://github.com/edwardhallam/luma-engine"
            target="_blank"
          >
            View on GitHub
          </Button>
          <Button variant="contained" startIcon={<Add />}>
            Add Task
          </Button>
        </Box>
      </Box>

      <DragDropContext onDragEnd={handleDragEnd}>
        <Grid container spacing={3}>
          {COLUMN_ORDER.map((status) => (
            <Grid item xs={12} sm={6} md={3} key={status}>
              <Paper sx={{ p: 2, height: 'fit-content', minHeight: 600 }}>
                <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                  <Typography variant="h6" fontWeight="bold">
                    {status}
                  </Typography>
                  <Chip
                    label={itemsByStatus[status].length}
                    size="small"
                    color={
                      status === 'Review' ? 'warning' :
                      status === 'Ready' ? 'primary' :
                      status === 'In Progress' ? 'info' : 'success'
                    }
                  />
                </Box>

                <Droppable droppableId={status}>
                  {(provided, snapshot) => (
                    <Box
                      ref={provided.innerRef}
                      {...provided.droppableProps}
                      sx={{
                        backgroundColor: snapshot.isDraggingOver ? 'action.hover' : 'transparent',
                        borderRadius: 1,
                        minHeight: 500,
                        p: 1,
                      }}
                    >
                      {itemsByStatus[status].map((item, index) => (
                        <Draggable key={item.id} draggableId={item.id} index={index}>
                          {(provided, snapshot) => (
                            <Card
                              ref={provided.innerRef}
                              {...provided.draggableProps}
                              {...provided.dragHandleProps}
                              sx={{
                                mb: 2,
                                opacity: snapshot.isDragging ? 0.8 : 1,
                                transform: snapshot.isDragging ? 'rotate(5deg)' : 'none',
                                cursor: 'grab',
                                '&:hover': {
                                  boxShadow: 4,
                                },
                              }}
                            >
                              <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
                                <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={1}>
                                  <Typography variant="body1" fontWeight="medium" sx={{ flexGrow: 1 }}>
                                    {item.title}
                                  </Typography>
                                  <IconButton size="small" onClick={() => handleEditItem(item)}>
                                    <MoreVert fontSize="small" />
                                  </IconButton>
                                </Box>

                                <Typography variant="body2" color="textSecondary" mb={2} sx={{
                                  display: '-webkit-box',
                                  overflow: 'hidden',
                                  WebkitBoxOrient: 'vertical',
                                  WebkitLineClamp: 3,
                                }}>
                                  {item.description}
                                </Typography>

                                <Box display="flex" gap={1} mb={2} flexWrap="wrap">
                                  <Chip
                                    label={item.priority}
                                    size="small"
                                    sx={{
                                      backgroundColor: PRIORITY_COLORS[item.priority],
                                      color: 'white',
                                      fontSize: '0.7rem',
                                    }}
                                  />
                                  <Chip
                                    label={item.size}
                                    size="small"
                                    sx={{
                                      backgroundColor: SIZE_COLORS[item.size],
                                      color: 'white',
                                      fontSize: '0.7rem',
                                    }}
                                  />
                                  <Chip
                                    label={`${item.estimate}d`}
                                    size="small"
                                    variant="outlined"
                                    sx={{ fontSize: '0.7rem' }}
                                  />
                                </Box>

                                <Box display="flex" justifyContent="space-between" alignItems="center">
                                  <Box display="flex" gap={0.5}>
                                    {item.assignees.map((assignee, i) => (
                                      <Avatar
                                        key={i}
                                        sx={{ width: 24, height: 24, fontSize: '0.8rem' }}
                                      >
                                        {assignee[0].toUpperCase()}
                                      </Avatar>
                                    ))}
                                  </Box>

                                  <Typography variant="caption" color="textSecondary">
                                    #{item.id.slice(-4)}
                                  </Typography>
                                </Box>
                              </CardContent>
                            </Card>
                          )}
                        </Draggable>
                      ))}
                      {provided.placeholder}
                    </Box>
                  )}
                </Droppable>
              </Paper>
            </Grid>
          ))}
        </Grid>
      </DragDropContext>

      {/* Edit Item Dialog */}
      <Dialog
        open={isEditDialogOpen}
        onClose={() => setIsEditDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Edit Task</DialogTitle>
        <DialogContent>
          {selectedItem && (
            <Box sx={{ pt: 2 }}>
              <TextField
                fullWidth
                label="Title"
                value={selectedItem.title}
                onChange={(e) =>
                  setSelectedItem({ ...selectedItem, title: e.target.value })
                }
                sx={{ mb: 2 }}
              />

              <TextField
                fullWidth
                multiline
                rows={4}
                label="Description"
                value={selectedItem.description}
                onChange={(e) =>
                  setSelectedItem({ ...selectedItem, description: e.target.value })
                }
                sx={{ mb: 2 }}
              />

              <Grid container spacing={2}>
                <Grid item xs={6} md={3}>
                  <FormControl fullWidth>
                    <InputLabel>Status</InputLabel>
                    <Select
                      value={selectedItem.status}
                      onChange={(e) =>
                        setSelectedItem({
                          ...selectedItem,
                          status: e.target.value as WorkflowItem['status'],
                        })
                      }
                    >
                      {COLUMN_ORDER.map((status) => (
                        <MenuItem key={status} value={status}>
                          {status}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </Grid>

                <Grid item xs={6} md={3}>
                  <FormControl fullWidth>
                    <InputLabel>Priority</InputLabel>
                    <Select
                      value={selectedItem.priority}
                      onChange={(e) =>
                        setSelectedItem({
                          ...selectedItem,
                          priority: e.target.value as WorkflowItem['priority'],
                        })
                      }
                    >
                      <MenuItem value="High">High</MenuItem>
                      <MenuItem value="Medium">Medium</MenuItem>
                      <MenuItem value="Low">Low</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>

                <Grid item xs={6} md={3}>
                  <FormControl fullWidth>
                    <InputLabel>Size</InputLabel>
                    <Select
                      value={selectedItem.size}
                      onChange={(e) =>
                        setSelectedItem({
                          ...selectedItem,
                          size: e.target.value as WorkflowItem['size'],
                        })
                      }
                    >
                      <MenuItem value="Small">Small</MenuItem>
                      <MenuItem value="Medium">Medium</MenuItem>
                      <MenuItem value="Large">Large</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>

                <Grid item xs={6} md={3}>
                  <TextField
                    fullWidth
                    type="number"
                    label="Estimate (days)"
                    value={selectedItem.estimate}
                    onChange={(e) =>
                      setSelectedItem({
                        ...selectedItem,
                        estimate: parseInt(e.target.value) || 0,
                      })
                    }
                  />
                </Grid>
              </Grid>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setIsEditDialogOpen(false)}>Cancel</Button>
          <Button variant="contained" onClick={handleUpdateItem}>
            Save Changes
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  )
}
