import React, { useEffect, useState } from 'react';
import api from '../api';
import {
  Container, Box, Typography, Card, CardContent, Rating, Grid, Skeleton
} from '@mui/material';

export default function FeedbackList() {
  const [list, setList] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    api.get('/feedback')
      .then(response => {
        if (!Array.isArray(response.data)) {
          throw new Error('Unexpected response format');
        }
        setList(response.data);
        setError(null);
      })
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (error) {
    return <Typography color="error">Error: {error}</Typography>;
  }

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>Feedback Received</Typography>
      <Grid container spacing={2}>
        {loading ? (
          // Show skeleton loaders while loading
          Array.from(new Array(6)).map((_, index) => (
            <Grid key={index} item xs={12} sm={6}>
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                    <Skeleton variant="text" width="40%" height={32} />
                    <Skeleton variant="rectangular" width={100} height={20} />
                  </Box>
                  <Skeleton variant="text" width="100%" />
                  <Skeleton variant="text" width="80%" />
                </CardContent>
              </Card>
            </Grid>
          ))
        ) : (
          // Show actual data after loading
          list.map(f => (
            <Grid key={f.id} item xs={12} sm={6}>
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                    <Typography variant="h6">{f.name || 'Anonymous'}</Typography>
                    <Rating value={f.rating || 0} readOnly size="small" />
                  </Box>
                  <Typography variant="body1" sx={{ mt: 1 }}>
                    {f.message}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))
        )}
      </Grid>
    </Container>
  );
}
