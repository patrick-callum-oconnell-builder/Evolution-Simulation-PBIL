import React from 'react';
import {
  Paper,
  Box,
  Typography,
  Chip,
  Grid,
  LinearProgress,
  Alert
} from '@mui/material';
import {
  Wifi,
  WifiOff,
  PlayCircle,
  PauseCircle,
  Timer,
  TrendingUp
} from '@mui/icons-material';

const StatusPanel = ({ 
  isConnected, 
  isRunning, 
  generation, 
  fitness, 
  maxFitness, 
  timeElapsed, 
  error 
}) => {
  const getConnectionStatus = () => {
    if (error) {
      return { 
        color: 'error', 
        icon: <WifiOff />, 
        label: 'Connection Error',
        variant: 'outlined'
      };
    }
    if (isConnected) {
      return { 
        color: 'success', 
        icon: <Wifi />, 
        label: 'Connected',
        variant: 'filled'
      };
    }
    return { 
      color: 'warning', 
      icon: <WifiOff />, 
      label: 'Disconnected',
      variant: 'outlined'
    };
  };

  const getRunningStatus = () => {
    if (isRunning) {
      return { 
        color: 'primary', 
        icon: <PlayCircle />, 
        label: 'Running',
        variant: 'filled'
      };
    }
    return { 
      color: 'default', 
      icon: <PauseCircle />, 
      label: 'Stopped',
      variant: 'outlined'
    };
  };

  const connectionStatus = getConnectionStatus();
  const runningStatus = getRunningStatus();

  const fitnessProgress = maxFitness > 0 ? (fitness / maxFitness) * 100 : 0;

  const formatTime = (seconds) => {
    if (!seconds || seconds < 1) return '0s';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return mins > 0 ? `${mins}m ${secs}s` : `${secs}s`;
  };

  return (
    <Paper sx={{ p: 2 }}>
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}
      
      <Grid container spacing={3} alignItems="center">
        {/* Connection Status */}
        <Grid item xs={12} sm={6} md={3}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Typography variant="body2" color="text.secondary">
              Connection:
            </Typography>
            <Chip
              icon={connectionStatus.icon}
              label={connectionStatus.label}
              color={connectionStatus.color}
              variant={connectionStatus.variant}
              size="small"
            />
          </Box>
        </Grid>

        {/* Algorithm Status */}
        <Grid item xs={12} sm={6} md={3}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Typography variant="body2" color="text.secondary">
              Algorithm:
            </Typography>
            <Chip
              icon={runningStatus.icon}
              label={runningStatus.label}
              color={runningStatus.color}
              variant={runningStatus.variant}
              size="small"
            />
          </Box>
        </Grid>

        {/* Generation Counter */}
        <Grid item xs={12} sm={6} md={3}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <TrendingUp fontSize="small" color="action" />
            <Typography variant="body2" color="text.secondary">
              Generation:
            </Typography>
            <Typography variant="body2" fontWeight="bold">
              {generation}
            </Typography>
          </Box>
        </Grid>

        {/* Timer */}
        <Grid item xs={12} sm={6} md={3}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Timer fontSize="small" color="action" />
            <Typography variant="body2" color="text.secondary">
              Time:
            </Typography>
            <Typography variant="body2" fontWeight="bold">
              {formatTime(timeElapsed)}
            </Typography>
          </Box>
        </Grid>
      </Grid>

      {/* Fitness Progress */}
      {maxFitness > 0 && (
        <Box sx={{ mt: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 1 }}>
            <Typography variant="body2" color="text.secondary">
              Fitness Progress
            </Typography>
            <Typography variant="body2" fontWeight="bold">
              {fitness}/{maxFitness} ({fitnessProgress.toFixed(1)}%)
            </Typography>
          </Box>
          <LinearProgress
            variant="determinate"
            value={fitnessProgress}
            sx={{
              height: 8,
              borderRadius: 4,
              bgcolor: 'action.hover',
              '& .MuiLinearProgress-bar': {
                borderRadius: 4,
                bgcolor: fitnessProgress === 100 ? 'success.main' : 'primary.main'
              }
            }}
          />
          {fitnessProgress === 100 && (
            <Typography variant="body2" color="success.main" sx={{ mt: 1, textAlign: 'center' }}>
              🎉 Optimal solution found!
            </Typography>
          )}
        </Box>
      )}

      {/* Quick Stats */}
      {isRunning && generation > 0 && (
        <Box sx={{ mt: 2, display: 'flex', gap: 2, flexWrap: 'wrap' }}>
          <Chip
            label={`Gen/s: ${timeElapsed > 0 ? (generation / timeElapsed).toFixed(1) : '0'}`}
            size="small"
            variant="outlined"
          />
          {fitnessProgress > 0 && (
            <Chip
              label={`${fitnessProgress.toFixed(0)}% complete`}
              size="small"
              variant="outlined"
              color={fitnessProgress > 75 ? 'success' : fitnessProgress > 25 ? 'warning' : 'default'}
            />
          )}
        </Box>
      )}
    </Paper>
  );
};

export default StatusPanel; 