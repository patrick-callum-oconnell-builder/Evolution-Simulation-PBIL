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
          height: 150, 
          display: 'flex', 
          flexDirection: 'column',
          alignItems: 'center', 
          justifyContent: 'center',
          bgcolor: 'background.default',
          borderRadius: 1,
          gap: 1.5
        }}
      >
        <CircularProgress size={32} />
        <Typography variant="body2" color="text.secondary" textAlign="center" sx={{ fontSize: '0.85rem' }}>
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
      <Paper sx={{ p: 1.5, mb: 1.5, bgcolor: isOptimal ? 'success.dark' : 'background.paper' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 0.5 }}>
          <Typography variant="subtitle1" color={isOptimal ? 'success.contrastText' : 'text.primary'}>
            {isOptimal ? '🎉 Optimal!' : '🎯 Current Best'}
          </Typography>
          <Chip
            icon={<TrendingUp />}
            label={`${fitnessPercentage.toFixed(1)}%`}
            color={isOptimal ? 'success' : fitnessPercentage > 75 ? 'warning' : 'default'}
            variant="filled"
            size="small"
          />
        </Box>
        
        <Typography 
          variant="body2" 
          fontWeight="bold"
          color={isOptimal ? 'success.contrastText' : 'text.primary'}
        >
          {fitness} / {maxFitness} clauses satisfied
        </Typography>
        
        {isOptimal && (
          <Typography variant="body2" color="success.contrastText" sx={{ mt: 0.5, fontSize: '0.8rem' }}>
            All clauses satisfied! This is the optimal solution.
          </Typography>
        )}
      </Paper>

      {/* Variable Assignment */}
      <Typography variant="body2" gutterBottom sx={{ fontSize: '0.9rem', fontWeight: 'bold' }}>
        Variable Assignment:
      </Typography>
      
      <Box sx={{ mb: 1.5, maxHeight: 200, overflowY: 'auto' }}>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
          {solution.map((value, index) => (
            <Tooltip
              key={index}
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
                  minWidth: 45,
                  height: 24,
                  fontSize: '0.7rem',
                  fontWeight: 'bold',
                  cursor: 'help',
                  '& .MuiChip-icon': {
                    fontSize: '0.8rem'
                  }
                }}
              />
            </Tooltip>
          ))}
        </Box>
      </Box>

      {/* Solution String */}
      <Typography variant="body2" gutterBottom sx={{ fontSize: '0.9rem', fontWeight: 'bold' }}>
        Binary Vector:
      </Typography>
      <Paper 
        sx={{ 
          p: 0.8, 
          bgcolor: 'background.default',
          fontFamily: 'monospace',
          fontSize: '0.75rem',
          overflow: 'auto',
          mb: 1.5,
          maxHeight: 60
        }}
      >
        <Typography component="span" sx={{ fontFamily: 'inherit', lineHeight: 1.2 }}>
          [{solution.join(', ')}]
        </Typography>
      </Paper>

      {/* Solution Statistics */}
      <Box sx={{ display: 'flex', gap: 0.5, flexWrap: 'wrap', mb: 1 }}>
        <Chip
          label={`${solution.length} variables`}
          size="small"
          variant="outlined"
          sx={{ fontSize: '0.7rem', height: 20 }}
        />
        <Chip
          label={`${solution.filter(v => v === 1).length} TRUE`}
          size="small"
          variant="outlined"
          color="success"
          sx={{ fontSize: '0.7rem', height: 20 }}
        />
        <Chip
          label={`${solution.filter(v => v === 0).length} FALSE`}
          size="small"
          variant="outlined"
          color="error"
          sx={{ fontSize: '0.7rem', height: 20 }}
        />
      </Box>

      {/* Additional Info */}
      {!isOptimal && fitness > 0 && (
        <Box sx={{ mt: 1, p: 0.8, bgcolor: 'action.hover', borderRadius: 1 }}>
          <Typography variant="body2" color="text.secondary" sx={{ fontSize: '0.75rem' }}>
            💡 This solution satisfies {fitness} out of {maxFitness} clauses. 
            {maxFitness - fitness} clauses still need to be satisfied.
          </Typography>
        </Box>
      )}
    </Box>
  );
};

export default SolutionDisplay; 