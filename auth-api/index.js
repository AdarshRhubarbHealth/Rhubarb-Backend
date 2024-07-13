const express = require('express');
const mongoose = require('mongoose');
const config = require('config');
const authRoutes = require('./routes/auth');
const bodyParser = require('body-parser');

const app = express();
const PORT = process.env.PORT || 5000;

// Body parser middleware
app.use(bodyParser.json());

// Connect to MongoDB
mongoose.connect(config.get('MONGODB_URI'), {
    useNewUrlParser: true,
    useUnifiedTopology: true
}).then(() => console.log('Connected to MongoDB'))
  .catch(err => console.log('Failed to connect to MongoDB', err));

// Use routes
app.use('/api/auth', authRoutes);

// Start server
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
