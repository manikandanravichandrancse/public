import React, { useState } from 'react';
import { useFormik } from 'formik';
import * as Yup from 'yup';
import api from '../api';
import {
  Container, Box, TextField, Button, Typography, Rating, Paper
} from '@mui/material';

export default function FeedbackPost() {
  const [success, setSuccess] = useState(null);
  const [error, setError] = useState(null);

  const formik = useFormik({
    initialValues: {
      name: '',
      email: '',
      mobile: '',
      message: '',
      rating: 0,
    },
    validationSchema: Yup.object({
      name: Yup.string().required('Name is required'),
      email: Yup.string()
        .email('Invalid email address')
        .required('Email is required'),
      message: Yup.string()
        .min(10, 'Message must be at least 10 characters')
        .max(500, 'Message cannot exceed 500 characters')
        .required('Message is required'),
      mobile: Yup.string().required('Mobile Number is required'),
      rating: Yup.number()
        .min(1, 'Rating must be greater than zero')
        .required('Rating is required'),
    }),
    onSubmit: async (values, { resetForm }) => {
      try {
        await api.post('/feedback', values);
        setSuccess('Feedback submitted successfully');
        setError(null);
        resetForm();
      } catch {
        setError('Failed to submit feedback');
        setSuccess(null);
      }
    },
  });

  return (
    <Container maxWidth="sm" sx={{ mt: 4 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h4" gutterBottom>
          Give Your Feedback
        </Typography>
        {success && <Typography color="success.main">{success}</Typography>}
        {error && <Typography color="error.main">{error}</Typography>}
        <Box component="form" noValidate onSubmit={formik.handleSubmit}>
          <TextField
            fullWidth
            label="Name"
            name="name"
            value={formik.values.name}
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            margin="normal"
            error={formik.touched.name && Boolean(formik.errors.name)}
            helperText={formik.touched.name && formik.errors.name}
          />
          <TextField
            fullWidth
            label="Email"
            name="email"
            type="email"
            value={formik.values.email}
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            margin="normal"
            error={formik.touched.email && Boolean(formik.errors.email)}
            helperText={formik.touched.email && formik.errors.email}
          />
          <TextField
            fullWidth
            label="Mobile"
            name="mobile"
            value={formik.values.mobile}
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            margin="normal"
            error={formik.touched.mobile && Boolean(formik.errors.mobile)}
            helperText={formik.touched.mobile && formik.errors.mobile}
          />
          <TextField
            fullWidth
            label="Message"
            name="message"
            multiline
            minRows={4}
            value={formik.values.message}
            onChange={formik.handleChange}
            onBlur={formik.handleBlur}
            margin="normal"
            error={formik.touched.message && Boolean(formik.errors.message)}
            helperText={formik.touched.message && formik.errors.message}
          />
          <Box sx={{ display: 'flex', alignItems: 'center', my: 2 }}>
            <Typography component="legend">Rating</Typography>
            <Rating
              name="rating"
              value={formik.values.rating}
              onChange={(e, value) => formik.setFieldValue('rating', value)}
              onBlur={formik.handleBlur}
            />
          </Box>
          {formik.touched.rating && formik.errors.rating && (
            <Typography sx={{ color: 'error.main', mb: 2 }}>
              {formik.errors.rating}
            </Typography>
          )}
          <Button type="submit" variant="contained" color="primary" fullWidth size="large">
            Submit Feedback
          </Button>
        </Box>
      </Paper>
    </Container>
  );
}
