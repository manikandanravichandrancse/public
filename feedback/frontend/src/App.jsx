// src/App.jsx
import React from 'react';
import { Routes, Route, NavLink } from 'react-router-dom';
import {
  AppBar, Toolbar, Typography, Button, Container
} from '@mui/material';
import FeedbackPost from './pages/FeedbackPost';
import FeedbackList from './pages/FeedbackList';

export default function App() {
  const activeStyle = {
    fontWeight: 'bold',
    color: 'yellow',
  };

  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            Feedback App
          </Typography>

          <Button
            color="inherit"
            component={NavLink}
            to="/"
            end
            style={({ isActive }) => (isActive ? activeStyle : undefined)}
          >
            List
          </Button>

          <Button
            color="inherit"
            component={NavLink}
            to="/post"
            style={({ isActive }) => (isActive ? activeStyle : undefined)}
          >
            Post
          </Button>
        </Toolbar>
      </AppBar>
      <Container sx={{ mt: 4 }}>
        <Routes>
          <Route path="/" element={<FeedbackList />} />
          <Route path="/post" element={<FeedbackPost />} />
        </Routes>
      </Container>
    </>
  );
}
