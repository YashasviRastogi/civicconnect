const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const multer = require('multer');
const path = require('path');
require('dotenv').config();
  
const app = express();
app.use(cors());
app.use(express.json());
app.use('/uploads', express.static('uploads'));

mongoose.connect(process.env.MONGO_URI, { useNewUrlParser: true });

const upload = multer({ dest: 'uploads/' });

const IssueSchema = new mongoose.Schema({
  title: String,
  description: String,
  image: String,
  lat: Number,
  lng: Number,
  ward: String,
  councilor: { name: String, phone: String, email: String },
  status: { type: String, default: 'open' },
  createdAt: { type: Date, default: Date.now }
});
const Issue = mongoose.model('Issue', IssueSchema);

app.post('/api/issues', upload.single('image'), async (req, res) => {
  const { title, description, lat, lng } = req.body;
  const image = req.file ? `/uploads/${req.file.filename}` : null;
  
  const geocoder = require('node-geocoder')({ 
    provider: 'google', apiKey: process.env.GOOGLE_API_KEY 
  });
  const geo = await geocoder.reverse({ lat, lng });
  const ward = geo.data[0]?.administrativeLevels?.level2 || 'Unknown';
  
  const councilor = await fetchCouncilor(ward);
  
  const issue = new Issue({ title, description, image, lat: parseFloat(lat), lng: parseFloat(lng), ward, councilor });
  await issue.save();
  res.json(issue);
});

app.get('/api/issues', async (req, res) => {
  const issues = await Issue.find({ status: 'open' });
  res.json(issues);
});

async function fetchCouncilor(ward) {
  return { name: 'John Doe', phone: '1234567890', email: 'councilor@example.com' };
}

app.listen(5000, () => console.log('Server on port 5000'));
