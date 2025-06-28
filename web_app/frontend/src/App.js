import React, { useState, useEffect, useCallback } from 'react';
import {
  ThemeProvider,
  createTheme,
  CssBaseline,
  Container,
  Paper,
  Typography,
  Grid,
  Box,
  AppBar,
  Toolbar,
  IconButton,
  Alert,
  Snackbar
} from '@mui/material';
import {
  PlayArrow,
  Stop,
  Settings,
  Timeline,
  DataArray
} from '@mui/icons-material';

import useWebSocket from './hooks/useWebSocket';
import ParameterPanel from './components/ParameterPanel';
import FitnessChart from './components/FitnessChart';
import ProbabilityHeatmap from './components/ProbabilityHeatmap';
import StatusPanel from './components/StatusPanel';
import SolutionDisplay from './components/SolutionDisplay';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#90caf9',
    },
    secondary: {
      main: '#f48fb1',
    },
    background: {
      default: '#1a1a2e',
      paper: '#16213e',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
  },
});

function App() {
  const [pbilConfig, setPbilConfig] = useState({
    cnf_file: 'sample_problem.cnf',
    pop_size: 100,
    learning_rate: 0.1,
    negative_learning_rate: 0.075,
    mutation_probability: 0.02,
    mutation_shift: 0.05,
    max_iterations: 1000,
  });

  const [pbilData, setPbilData] = useState({
    isRunning: false,
    currentGeneration: 0,
    fitnessHistory: [],
    probabilityHistory: [],
    bestSolution: [],
    currentFitness: 0,
    maxFitness: 0,
    timeElapsed: 0,
  });

  const [notification, setNotification] = useState({ open: false, message: '', severity: 'info' });

  const wsUrl = `ws://localhost:8000/ws/pbil`;
  const { isConnected, messages, error, sendMessage, clearMessages } = useWebSocket(wsUrl);

  // Process WebSocket messages
  useEffect(() => {
    if (messages.length > 0) {
      const latestMessage = messages[messages.length - 1];
      
      switch (latestMessage.type) {
        case 'status':
          setNotification({
            open: true,
            message: latestMessage.message,
            severity: 'info'
          });
          setPbilData(prev => ({ ...prev, isRunning: true }));
          break;
          
        case 'progress':
          const progressData = latestMessage.data;
          setPbilData(prev => ({
            ...prev,
            currentGeneration: progressData.generation,
            fitnessHistory: [...prev.fitnessHistory, {
              generation: progressData.generation,
              fitness: progressData.best_fitness,
              maxFitness: progressData.max_fitness
            }],
            probabilityHistory: [...prev.probabilityHistory, {
              generation: progressData.generation,
              probabilities: progressData.probability_vector
            }],
            bestSolution: progressData.best_individual,
            currentFitness: progressData.best_fitness,
            maxFitness: progressData.max_fitness,
          }));
          break;
          
        case 'complete':
          const finalData = latestMessage.data;
          setPbilData(prev => ({ 
            ...prev, 
            isRunning: false,
            timeElapsed: finalData.time_elapsed || 0,
            currentFitness: finalData.fitness || prev.currentFitness,
            maxFitness: finalData.max_fitness || prev.maxFitness,
            bestSolution: finalData.best_solution || prev.bestSolution
          }));
          setNotification({
            open: true,
            message: `PBIL completed! Final fitness: ${finalData.fitness}/${finalData.max_fitness}`,
            severity: 'success'
          });
          break;
          
        case 'error':
          setPbilData(prev => ({ ...prev, isRunning: false }));
          setNotification({
            open: true,
            message: `Error: ${latestMessage.message}`,
            severity: 'error'
          });
          break;
          
        case 'stopped':
          setPbilData(prev => ({ ...prev, isRunning: false }));
          setNotification({
            open: true,
            message: 'PBIL execution stopped',
            severity: 'warning'
          });
          break;
          
        default:
          console.log('Unknown message type:', latestMessage.type);
      }
    }
  }, [messages]);

  const handleStartPBIL = useCallback(() => {
    if (!isConnected) {
      setNotification({
        open: true,
        message: 'Not connected to server',
        severity: 'error'
      });
      return;
    }

    // Clear previous data
    setPbilData(prev => ({
      ...prev,
      fitnessHistory: [],
      probabilityHistory: [],
      currentGeneration: 0,
    }));
    clearMessages();

    // Send start command
    sendMessage({
      action: 'start',
      config: pbilConfig
    });
  }, [isConnected, pbilConfig, sendMessage, clearMessages]);

  const handleStopPBIL = useCallback(() => {
    sendMessage({ action: 'stop' });
  }, [sendMessage]);

  const handleConfigChange = useCallback((newConfig) => {
    setPbilConfig(newConfig);
  }, []);

  const handleCloseNotification = () => {
    setNotification(prev => ({ ...prev, open: false }));
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ flexGrow: 1, minHeight: '100vh' }}>
        <AppBar position="static" elevation={0}>
          <Toolbar>
            <Timeline sx={{ mr: 2 }} />
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              PBIL Real-time Visualization
            </Typography>
            <IconButton
              color="inherit"
              onClick={pbilData.isRunning ? handleStopPBIL : handleStartPBIL}
              disabled={!isConnected}
            >
              {pbilData.isRunning ? <Stop /> : <PlayArrow />}
            </IconButton>
          </Toolbar>
        </AppBar>

        <Container maxWidth="xl" sx={{ mt: 3, mb: 3 }}>
          <Grid container spacing={3}>
            {/* Status Panel */}
            <Grid item xs={12}>
              <StatusPanel 
                isConnected={isConnected}
                isRunning={pbilData.isRunning}
                generation={pbilData.currentGeneration}
                fitness={pbilData.currentFitness}
                maxFitness={pbilData.maxFitness}
                timeElapsed={pbilData.timeElapsed}
                error={error}
              />
            </Grid>

            {/* Parameter Panel */}
            <Grid item xs={12} md={4}>
              <Paper sx={{ p: 2, height: 'fit-content' }}>
                <Typography variant="h6" gutterBottom>
                  <Settings sx={{ mr: 1, verticalAlign: 'middle' }} />
                  Algorithm Parameters
                </Typography>
                <ParameterPanel
                  config={pbilConfig}
                  onChange={handleConfigChange}
                  disabled={pbilData.isRunning}
                  onStart={handleStartPBIL}
                  onStop={handleStopPBIL}
                  isRunning={pbilData.isRunning}
                  isConnected={isConnected}
                />
              </Paper>
            </Grid>

            {/* Fitness Chart - Full width */}
            <Grid item xs={12} md={8}>
              <Paper sx={{ p: 2 }}>
                <Typography variant="h6" gutterBottom>
                  <Timeline sx={{ mr: 1, verticalAlign: 'middle' }} />
                  Fitness Evolution
                </Typography>
                <FitnessChart data={pbilData.fitnessHistory} />
              </Paper>
            </Grid>

            {/* Probability Vector Heatmap */}
            <Grid item xs={12} md={8}>
              <Paper sx={{ p: 2 }}>
                <Typography variant="h6" gutterBottom>
                  <DataArray sx={{ mr: 1, verticalAlign: 'middle' }} />
                  Probability Vector Evolution
                </Typography>
                <ProbabilityHeatmap data={pbilData.probabilityHistory} />
              </Paper>
            </Grid>

            {/* Current Solution - Moved to bottom right */}
            <Grid item xs={12} md={4}>
              <Paper sx={{ p: 2, height: 'fit-content' }}>
                <Typography variant="h6" gutterBottom>
                  Current Best Solution
                </Typography>
                <SolutionDisplay 
                  solution={pbilData.bestSolution}
                  fitness={pbilData.currentFitness}
                  maxFitness={pbilData.maxFitness}
                />
              </Paper>
            </Grid>
          </Grid>
        </Container>
      </Box>

      {/* Notifications */}
      <Snackbar
        open={notification.open}
        autoHideDuration={6000}
        onClose={handleCloseNotification}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert 
          onClose={handleCloseNotification} 
          severity={notification.severity}
          variant="filled"
        >
          {notification.message}
        </Alert>
      </Snackbar>
    </ThemeProvider>
  );
}

export default App; 