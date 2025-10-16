import axios from 'axios';

export default axios.create({
  baseURL: 'http://localhost:8000/api/latest',  // exactly your backend prefix
  headers: { 'Content-Type': 'application/json' },
});
