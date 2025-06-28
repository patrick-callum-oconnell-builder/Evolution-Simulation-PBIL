import React from 'react';
import {
  Box,
  Typography,
  Chip,
  Grid,
  Paper,
  Tooltip,
  CircularProgress
} from '@mui/material';
import {
  CheckCircle,
  Cancel,
  TrendingUp
} from '@mui/icons-material';

const SolutionDisplay = ({ solution, fitness, maxFitness }) => {
  if (!solution || solution.length === 0) {
    return (
      <Box 
        sx={{ 
          height: 200, 
          display: 'flex', 
          flexDirection: 'column',
          alignItems: 'center', 
          justifyContent: 'center',
          bgcolor: 'background.default',
          borderRadius: 1,
          gap: 2
        }}
      >
        <CircularProgress size={40} />
        <Typography variant="body2" color="text.secondary" textAlign="center">
          Solution will appear here when PBIL starts running...
        </Typography>
      </Box>
    );
  }

  const fitnessPercentage = maxFitness > 0 ? (fitness / maxFitness) * 100 : 0;
  const isOptimal = fitness === maxFitness && maxFitness > 0;

  const getVariableColor = (value, index) => {
    if (value === 1) {
      return 'success';
    } else if (value === 0) {
      return 'error';
    }
    return 'default';
  };

  const getVariableIcon = (value) => {
    if (value === 1) {
      return <CheckCircle fontSize="small" />;
    } else if (value === 0) {
      return <Cancel fontSize="small" />;
    }
    return null;
  };

  return (
    <Box>
      {/* Fitness Summary */}
      <Paper sx={{ p: 2, mb: 2, bgcolor: isOptimal ? 'success.dark' : 'background.paper' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 1 }}>
          <Typography variant="h6" color={isOptimal ? 'success.contrastText' : 'text.primary'}>
            {isOptimal ? '🎉 Optimal!' : '🎯 Current Best'}
          </Typography>
          <Chip
            icon={<TrendingUp />}
            label={`${fitnessPercentage.toFixed(1)}%`}
            color={isOptimal ? 'success' : fitnessPercentage > 75 ? 'warning' : 'default'}
            variant="filled"
          />
        </Box>
        
        <Typography 
          variant="body1" 
          fontWeight="bold"
          color={isOptimal ? 'success.contrastText' : 'text.primary'}
        >
          {fitness} / {maxFitness} clauses satisfied
        </Typography>
        
        {isOptimal && (
          <Typography variant="body2" color="success.contrastText" sx={{ mt: 1 }}>
            All clauses satisfied! This is the optimal solution.
          </Typography>
        )}
      </Paper>

      {/* Variable Assignment */}
      <Typography variant="subtitle2" gutterBottom>
        Variable Assignment:
      </Typography>
      
      <Box sx={{ mb: 2, maxHeight: 300, overflowY: 'auto' }}>
        <Grid container spacing={1}>
          {solution.map((value, index) => (
            <Grid item key={index}>
              <Tooltip
                title={`Variable x${index + 1} = ${value} ${value === 1 ? '(TRUE)' : '(FALSE)'}`}
                arrow
              >
                <Chip
                  icon={getVariableIcon(value)}
                  label={`x${index + 1}`}
                  color={getVariableColor(value, index)}
                  variant="filled"
                  size="small"
                  sx={{
                    minWidth: 60,
                    fontWeight: 'bold',
                    cursor: 'help'
                  }}
                />
              </Tooltip>
            </Grid>
          ))}
        </Grid>
      </Box>

      {/* Solution String */}
      <Typography variant="subtitle2" gutterBottom>
        Binary Vector:
      </Typography>
      <Paper 
        sx={{ 
          p: 1, 
          bgcolor: 'background.default',
          fontFamily: 'monospace',
          fontSize: '0.9rem',
          overflow: 'auto',
          mb: 2
        }}
      >
        <Typography component="span" sx={{ fontFamily: 'inherit' }}>
          [{solution.join(', ')}]
        </Typography>
      </Paper>

      {/* Solution Statistics */}
      <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
        <Chip
          label={`${solution.length} variables`}
          size="small"
          variant="outlined"
        />
        <Chip
          label={`${solution.filter(v => v === 1).length} TRUE`}
          size="small"
          variant="outlined"
          color="success"
        />
        <Chip
          label={`${solution.filter(v => v === 0).length} FALSE`}
          size="small"
          variant="outlined"
          color="error"
        />
      </Box>

      {/* Additional Info */}
      {!isOptimal && fitness > 0 && (
        <Box sx={{ mt: 2, p: 1, bgcolor: 'action.hover', borderRadius: 1 }}>
          <Typography variant="body2" color="text.secondary">
            💡 This solution satisfies {fitness} out of {maxFitness} clauses. 
            {maxFitness - fitness} clauses still need to be satisfied.
          </Typography>
        </Box>
      )}
    </Box>
  );
};

export default SolutionDisplay; 