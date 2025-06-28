import React, { useState, useEffect } from 'react';
import {
  TextField,
  Slider,
  Typography,
  Box,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Tooltip,
  IconButton,
  Button,
  Divider,
  ListSubheader,
  Chip
} from '@mui/material';
import { Info, PlayArrow, Stop, Psychology, Speed, LocalFireDepartment } from '@mui/icons-material';

const ParameterPanel = ({ config, onChange, disabled, onStart, onStop, isRunning, isConnected }) => {
  const [cnfFiles, setCnfFiles] = useState([]);
  const [loadingFiles, setLoadingFiles] = useState(true);

  // Fetch available CNF files
  useEffect(() => {
    const fetchCnfFiles = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/cnf-files');
        const data = await response.json();
        setCnfFiles(data.files || []);
      } catch (error) {
        console.error('Failed to fetch CNF files:', error);
        setCnfFiles([]);
      } finally {
        setLoadingFiles(false);
      }
    };

    fetchCnfFiles();
  }, []);

  const handleChange = (field) => (event) => {
    const value = event.target.value;
    onChange({
      ...config,
      [field]: field === 'cnf_file' ? value : Number(value)
    });
  };

  const handleSliderChange = (field) => (event, newValue) => {
    onChange({
      ...config,
      [field]: newValue
    });
  };

  // Get difficulty level and icon for CNF files
  const getDifficultyInfo = (fileName, size) => {
    if (fileName.includes('extreme') || fileName.includes('massive')) {
      return { level: 'Extreme', icon: <LocalFireDepartment color="error" fontSize="small" />, color: 'error' };
    } else if (fileName.includes('graph_coloring_25') || size > 3000) {
      return { level: 'Very Hard', icon: <LocalFireDepartment color="warning" fontSize="small" />, color: 'warning' };
    } else if (fileName.includes('30') || fileName.includes('graph_coloring')) {
      return { level: 'Hard', icon: <Speed color="info" fontSize="small" />, color: 'info' };
    } else if (fileName.includes('20') || fileName === 'sample_problem.cnf') {
      return { level: 'Medium', icon: <Psychology color="success" fontSize="small" />, color: 'success' };
    }
    return { level: 'Unknown', icon: <Psychology fontSize="small" />, color: 'default' };
  };

  const parameterInfo = {
    pop_size: "Number of individuals generated from probability vector each generation",
    learning_rate: "Rate at which probability vector moves toward best solutions",
    negative_learning_rate: "Rate at which probability vector moves away from worst solutions",
    mutation_probability: "Probability that each bit will be mutated",
    mutation_shift: "Amount by which probability values change during mutation",
    max_iterations: "Maximum number of generations before stopping"
  };

  const SliderWithInfo = ({ field, min, max, step, value, label }) => (
    <Box sx={{ mb: 3 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
        <Typography variant="body2" sx={{ flexGrow: 1 }}>
          {label}: {value}
        </Typography>
        <Tooltip title={parameterInfo[field]} arrow>
          <IconButton size="small">
            <Info fontSize="small" />
          </IconButton>
        </Tooltip>
      </Box>
      <Slider
        value={value}
        onChange={handleSliderChange(field)}
        min={min}
        max={max}
        step={step}
        disabled={disabled}
        valueLabelDisplay="auto"
        size="small"
      />
    </Box>
  );

  return (
    <Box>
      {/* Start/Stop Controls */}
      <Box sx={{ mb: 3, textAlign: 'center' }}>
        <Button
          variant="contained"
          size="large"
          startIcon={isRunning ? <Stop /> : <PlayArrow />}
          onClick={isRunning ? onStop : onStart}
          disabled={!isConnected}
          color={isRunning ? "error" : "primary"}
          sx={{ 
            minWidth: 120,
            mb: 2,
            fontSize: '1.1rem',
            boxShadow: 3,
            '&:hover': {
              boxShadow: 6,
            }
          }}
        >
          {isRunning ? 'Stop PBIL' : 'Start PBIL'}
        </Button>
        
        {!isConnected && (
          <Typography variant="body2" color="error" sx={{ mt: 1 }}>
            ⚠️ Not connected to server
          </Typography>
        )}
        
        {isRunning && (
          <Typography variant="body2" color="success.main" sx={{ mt: 1 }}>
            🔄 Algorithm running...
          </Typography>
        )}
      </Box>

      <Divider sx={{ mb: 3 }} />

      {/* CNF File Selection */}
      <FormControl fullWidth sx={{ mb: 3 }}>
        <InputLabel>MAXSAT Problem</InputLabel>
        <Select
          value={config.cnf_file}
          onChange={handleChange('cnf_file')}
          disabled={disabled || loadingFiles}
          label="MAXSAT Problem"
        >
          {loadingFiles ? (
            <MenuItem disabled>Loading problems...</MenuItem>
          ) : (
            (() => {
              const grouped = cnfFiles.reduce((acc, file) => {
                if (!acc[file.category]) acc[file.category] = [];
                acc[file.category].push(file);
                return acc;
              }, {});
              
              return Object.entries(grouped).map(([category, files]) => [
                <ListSubheader key={category} sx={{ bgcolor: 'background.paper' }}>
                  {category}
                </ListSubheader>,
                ...files.map(file => {
                  const difficulty = getDifficultyInfo(file.name, file.size);
                  return (
                    <MenuItem key={file.path} value={file.path}>
                      <Box sx={{ display: 'flex', alignItems: 'center', width: '100%', gap: 1 }}>
                        {difficulty.icon}
                        <Typography variant="body2" sx={{ flexGrow: 1, fontSize: '0.85rem' }}>
                          {file.name.replace('.cnf', '')}
                        </Typography>
                        <Chip 
                          label={difficulty.level} 
                          size="small" 
                          color={difficulty.color}
                          sx={{ height: 20, fontSize: '0.7rem' }}
                        />
                      </Box>
                    </MenuItem>
                  );
                })
              ]).flat();
            })()
          )}
        </Select>
        {config.cnf_file && !loadingFiles && (
          <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5 }}>
            {(() => {
              const file = cnfFiles.find(f => f.path === config.cnf_file);
              if (!file) return '';
              const difficulty = getDifficultyInfo(file.name, file.size);
              return `${difficulty.level} difficulty • ${(file.size / 1024).toFixed(1)}KB`;
            })()}
          </Typography>
        )}
      </FormControl>

      {/* Population Size */}
      <TextField
        fullWidth
        label="Population Size"
        type="number"
        value={config.pop_size}
        onChange={handleChange('pop_size')}
        disabled={disabled}
        InputProps={{ inputProps: { min: 10, max: 1000, step: 10 } }}
        sx={{ mb: 3 }}
        helperText={parameterInfo.pop_size}
      />

      {/* Learning Rate */}
      <SliderWithInfo
        field="learning_rate"
        min={0.01}
        max={0.5}
        step={0.01}
        value={config.learning_rate}
        label="Learning Rate"
      />

      {/* Negative Learning Rate */}
      <SliderWithInfo
        field="negative_learning_rate"
        min={0.01}
        max={0.3}
        step={0.005}
        value={config.negative_learning_rate}
        label="Negative Learning Rate"
      />

      {/* Mutation Probability */}
      <SliderWithInfo
        field="mutation_probability"
        min={0.001}
        max={0.1}
        step={0.001}
        value={config.mutation_probability}
        label="Mutation Probability"
      />

      {/* Mutation Shift */}
      <SliderWithInfo
        field="mutation_shift"
        min={0.01}
        max={0.2}
        step={0.005}
        value={config.mutation_shift}
        label="Mutation Shift"
      />

      {/* Max Iterations */}
      <TextField
        fullWidth
        label="Max Iterations"
        type="number"
        value={config.max_iterations}
        onChange={handleChange('max_iterations')}
        disabled={disabled}
        InputProps={{ inputProps: { min: 100, max: 10000, step: 100 } }}
        helperText={parameterInfo.max_iterations}
      />

      {/* Parameter Presets */}
      <Box sx={{ mt: 3 }}>
        <Typography variant="body2" gutterBottom>
          Quick Presets:
        </Typography>
        <Grid container spacing={1}>
          <Grid item xs={4}>
            <Typography
              variant="body2"
              sx={{ 
                cursor: disabled ? 'default' : 'pointer',
                color: disabled ? 'text.disabled' : 'primary.main',
                '&:hover': !disabled ? { textDecoration: 'underline' } : {}
              }}
              onClick={() => !disabled && onChange({
                ...config,
                pop_size: 50,
                learning_rate: 0.05,
                negative_learning_rate: 0.025,
                mutation_probability: 0.01,
                mutation_shift: 0.03
              })}
            >
              Conservative
            </Typography>
          </Grid>
          <Grid item xs={4}>
            <Typography
              variant="body2"
              sx={{ 
                cursor: disabled ? 'default' : 'pointer',
                color: disabled ? 'text.disabled' : 'primary.main',
                '&:hover': !disabled ? { textDecoration: 'underline' } : {}
              }}
              onClick={() => !disabled && onChange({
                ...config,
                pop_size: 100,
                learning_rate: 0.1,
                negative_learning_rate: 0.075,
                mutation_probability: 0.02,
                mutation_shift: 0.05
              })}
            >
              Balanced
            </Typography>
          </Grid>
          <Grid item xs={4}>
            <Typography
              variant="body2"
              sx={{ 
                cursor: disabled ? 'default' : 'pointer',
                color: disabled ? 'text.disabled' : 'primary.main',
                '&:hover': !disabled ? { textDecoration: 'underline' } : {}
              }}
              onClick={() => !disabled && onChange({
                ...config,
                pop_size: 200,
                learning_rate: 0.2,
                negative_learning_rate: 0.15,
                mutation_probability: 0.05,
                mutation_shift: 0.1
              })}
            >
              Aggressive
            </Typography>
          </Grid>
        </Grid>
      </Box>
    </Box>
  );
};

export default ParameterPanel; 