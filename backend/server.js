const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.get('/', (req, res) => {
  res.json({ message: 'CivicConnect Backend API is running!' });
});

// Add your API routes here
// Example: app.get('/api/issues', (req, res) => { ... });

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});