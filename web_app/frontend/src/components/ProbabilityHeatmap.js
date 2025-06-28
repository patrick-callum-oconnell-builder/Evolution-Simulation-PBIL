import React, { useMemo } from 'react';
import { Box, Typography, Tooltip, Chip } from '@mui/material';

const ProbabilityHeatmap = ({ data }) => {
  // Process data for heatmap visualization
  const { heatmapData, generations, variables, maxGen, currentProbabilities } = useMemo(() => {
    if (!data || data.length === 0) {
      return { heatmapData: [], generations: [], variables: [], maxGen: 0, currentProbabilities: [] };
    }

    const generations = data.map(d => d.generation);
    const maxGen = Math.max(...generations);
    const variables = data[0]?.probabilities ? 
      data[0].probabilities.map((_, i) => `x${i + 1}`) : [];
    
    const currentProbabilities = data[data.length - 1]?.probabilities || [];

    // Create heatmap matrix: [generation][variable] = probability
    const heatmapData = data.map(gen => ({
      generation: gen.generation,
      probabilities: gen.probabilities || []
    }));

    return { heatmapData, generations, variables, maxGen, currentProbabilities };
  }, [data]);

  // Color scale for probability values
  const getProbabilityColor = (probability) => {
    if (probability === undefined || probability === null) return '#1a1a2e';
    
    // Red to Yellow to Green scale
    const intensity = Math.abs(probability - 0.5) * 2; // 0 at 0.5, 1 at 0 or 1
    const hue = probability > 0.5 ? 120 : 0; // Green for >0.5, Red for <0.5
    const saturation = 60 + (intensity * 40); // 60-100%
    const lightness = 30 + (intensity * 30); // 30-60%
    
    return `hsl(${hue}, ${saturation}%, ${lightness}%)`;
  };

  // Cell size calculation
  const cellSize = 20;
  const cellGap = 1;

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
          Probability vector evolution will appear here when PBIL is running...
        </Typography>
      </Box>
    );
  }

  return (
    <Box>
      {/* Current Probabilities Summary */}
      <Box sx={{ mb: 2 }}>
        <Typography variant="body2" gutterBottom>
          Current Probability Vector (Generation {maxGen}):
        </Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
          {currentProbabilities.map((prob, i) => (
            <Chip
              key={i}
              label={`x${i + 1}: ${prob.toFixed(3)}`}
              size="small"
              sx={{
                bgcolor: getProbabilityColor(prob),
                color: prob > 0.3 && prob < 0.7 ? 'white' : 'black',
                fontSize: '0.7rem'
              }}
            />
          ))}
        </Box>
      </Box>

      {/* Legend */}
      <Box sx={{ mb: 2, display: 'flex', alignItems: 'center', gap: 2 }}>
        <Typography variant="body2">
          Probability:
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Box
            sx={{
              width: 15,
              height: 15,
              bgcolor: getProbabilityColor(0),
              border: '1px solid #666'
            }}
          />
          <Typography variant="caption">0.0</Typography>
          <Box
            sx={{
              width: 15,
              height: 15,
              bgcolor: getProbabilityColor(0.5),
              border: '1px solid #666'
            }}
          />
          <Typography variant="caption">0.5</Typography>
          <Box
            sx={{
              width: 15,
              height: 15,
              bgcolor: getProbabilityColor(1),
              border: '1px solid #666'
            }}
          />
          <Typography variant="caption">1.0</Typography>
        </Box>
      </Box>

      {/* Heatmap */}
      <Box sx={{ 
        overflowX: 'auto', 
        overflowY: 'auto',
        maxHeight: 400,
        border: '1px solid #333',
        borderRadius: 1,
        p: 1,
        bgcolor: 'background.default'
      }}>
        <Box sx={{ 
          display: 'grid',
          gridTemplateColumns: `50px repeat(${variables.length}, ${cellSize}px)`,
          gap: `${cellGap}px`,
          minWidth: 'fit-content'
        }}>
          {/* Header row */}
          <Box /> {/* Empty corner */}
          {variables.map((variable, i) => (
            <Box
              key={i}
              sx={{
                height: cellSize,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '0.7rem',
                fontWeight: 'bold',
                color: 'text.secondary'
              }}
            >
              {variable}
            </Box>
          ))}

          {/* Data rows */}
          {heatmapData.map((genData, genIndex) => (
            <React.Fragment key={genData.generation}>
              {/* Generation label */}
              <Box
                sx={{
                  height: cellSize,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '0.7rem',
                  fontWeight: 'bold',
                  color: 'text.secondary'
                }}
              >
                {genData.generation}
              </Box>

              {/* Probability cells */}
              {genData.probabilities.map((prob, varIndex) => (
                <Tooltip
                  key={varIndex}
                  title={`Gen ${genData.generation}, ${variables[varIndex]}: ${prob.toFixed(4)}`}
                  arrow
                >
                  <Box
                    sx={{
                      width: cellSize,
                      height: cellSize,
                      bgcolor: getProbabilityColor(prob),
                      border: '1px solid #444',
                      cursor: 'pointer',
                      borderRadius: 0.5,
                      '&:hover': {
                        border: '2px solid #fff',
                        zIndex: 1
                      }
                    }}
                  />
                </Tooltip>
              ))}
            </React.Fragment>
          ))}
        </Box>
      </Box>

      {/* Insights */}
      <Box sx={{ mt: 2 }}>
        <Typography variant="body2" color="text.secondary">
          {currentProbabilities.some(p => p > 0.8 || p < 0.2) && (
            "🎯 Some variables are converging (probabilities near 0 or 1)"
          )}
          {currentProbabilities.every(p => p > 0.3 && p < 0.7) && (
            "🔄 Probability vector still exploring (values near 0.5)"
          )}
        </Typography>
      </Box>
    </Box>
  );
};

export default ProbabilityHeatmap; 