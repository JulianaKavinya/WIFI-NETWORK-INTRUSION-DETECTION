const express = require('express');
const path = require('path');
const dotenv = require('dotenv');
const bodyParser = require('body-parser');
const alertRoutes = require('./routes/alertRoutes');
const cors = require('cors');


dotenv.config();

const app = express();

// Middleware to parse incoming JSON requests
app.use(express.json());
app.use(bodyParser.json()); // Optional, if express.json() is sufficient

app.use(cors({
    origin: ['http://localhost:3000', 'http://localhost:5000'], // Allow frontend and Python backend
    methods: ['GET', 'POST', 'PUT', 'DELETE'], // Allowed HTTP methods
}));

// Use the alert routes
app.use('/alerts', alertRoutes);

app.use((req, res, next) => {
    res.setHeader("Content-Security-Policy", "default-src 'none'; img-src 'self';");
    next();
  });

  // Handle GET request at the root URL
app.get('/', (req, res) => {
    res.send('Welcome to the WiFi Intrusion Detection System API');
});

  

// Set up the server port from environment variables or default to 2000
const PORT = process.env.PORT || 2000;

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
