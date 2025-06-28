import React from 'react';
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
  IconButton
} from '@mui/material';
import { Info } from '@mui/icons-material';

const ParameterPanel = ({ config, onChange, disabled }) => {
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
      {/* CNF File Selection */}
      <FormControl fullWidth sx={{ mb: 3 }}>
        <InputLabel>CNF File</InputLabel>
        <Select
          value={config.cnf_file}
          onChange={handleChange('cnf_file')}
          disabled={disabled}
          label="CNF File"
        >
          <MenuItem value="sample_problem.cnf">sample_problem.cnf</MenuItem>
        </Select>
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