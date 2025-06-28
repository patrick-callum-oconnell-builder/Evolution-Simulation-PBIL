import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine
} from 'recharts';
import { Box, Typography } from '@mui/material';

const FitnessChart = ({ data }) => {
  // If no data, show placeholder
  if (!data || data.length === 0) {
    return (
      <Box 
        sx={{ 
          height: 300, 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center',
          bgcolor: 'background.default',
          borderRadius: 1
        }}
      >
        <Typography variant="body2" color="text.secondary">
          Fitness data will appear here when PBIL is running...
        </Typography>
      </Box>
    );
  }

  // Calculate fitness percentage for better visualization
  const processedData = data.map(point => ({
    ...point,
    fitnessPercentage: point.maxFitness > 0 ? (point.fitness / point.maxFitness) * 100 : 0
  }));

  const maxFitness = data.length > 0 ? data[0].maxFitness : 0;
  const currentFitness = data.length > 0 ? data[data.length - 1].fitness : 0;
  const currentGeneration = data.length > 0 ? data[data.length - 1].generation : 0;

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <Box
          sx={{
            bgcolor: 'background.paper',
            border: '1px solid',
            borderColor: 'divider',
            borderRadius: 1,
            p: 1,
            boxShadow: 2
          }}
        >
          <Typography variant="body2">
            Generation: {label}
          </Typography>
          <Typography variant="body2" color="primary.main">
            Fitness: {data.fitness}/{data.maxFitness} ({data.fitnessPercentage.toFixed(1)}%)
          </Typography>
        </Box>
      );
    }
    return null;
  };

  return (
    <Box>
      {/* Statistics */}
      <Box sx={{ mb: 2, display: 'flex', gap: 3 }}>
        <Typography variant="body2">
          Generation: <strong>{currentGeneration}</strong>
        </Typography>
        <Typography variant="body2">
          Current Fitness: <strong>{currentFitness}/{maxFitness}</strong>
        </Typography>
        <Typography variant="body2">
          Progress: <strong>
            {maxFitness > 0 ? ((currentFitness / maxFitness) * 100).toFixed(1) : 0}%
          </strong>
        </Typography>
      </Box>

      {/* Chart */}
      <ResponsiveContainer width="100%" height={300}>
        <LineChart
          data={processedData}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#333" />
          <XAxis 
            dataKey="generation" 
            stroke="#888"
            fontSize={12}
          />
          <YAxis 
            stroke="#888"
            fontSize={12}
            domain={[0, maxFitness + 1]}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend />
          
          {/* Reference line for maximum fitness */}
          <ReferenceLine 
            y={maxFitness} 
            stroke="#ff6b6b" 
            strokeDasharray="5 5"
            label={{ value: "Target", position: "topLeft" }}
          />
          
          {/* Fitness line */}
          <Line
            type="monotone"
            dataKey="fitness"
            stroke="#90caf9"
            strokeWidth={2}
            dot={{ fill: '#90caf9', strokeWidth: 2, r: 3 }}
            activeDot={{ r: 5, fill: '#90caf9' }}
            name="Fitness"
          />
        </LineChart>
      </ResponsiveContainer>

      {/* Progress indicators */}
      <Box sx={{ mt: 2 }}>
        {currentFitness === maxFitness && maxFitness > 0 && (
          <Box
            sx={{
              bgcolor: 'success.dark',
              color: 'success.contrastText',
              p: 1,
              borderRadius: 1,
              textAlign: 'center'
            }}
          >
            <Typography variant="body2">
              🎉 Optimal solution found! All {maxFitness} clauses satisfied.
            </Typography>
          </Box>
        )}
        
        {data.length > 10 && currentFitness < maxFitness && (
          <Box sx={{ mt: 1 }}>
            <Typography variant="body2" color="text.secondary">
              {data.length > 1 && data[data.length - 1].fitness > data[data.length - 2].fitness && (
                "📈 Fitness improving..."
              )}
              {data.length > 5 && 
               data.slice(-5).every((point, i, arr) => i === 0 || point.fitness === arr[0].fitness) && (
                "⏸️ Fitness plateaued - consider adjusting parameters"
              )}
            </Typography>
          </Box>
        )}
      </Box>
    </Box>
  );
};

export default FitnessChart; 