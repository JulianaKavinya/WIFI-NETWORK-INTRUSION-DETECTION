require('dotenv').config();
const express = require('express');
const bodyParser = require('body-parser');
const alertRoutes = require('./routes/alertRoutes');


const app = express();
const PORT = 3000;

// Middleware to parse incoming JSON requests
app.use(express.json());

// Use alert routes
app.use("/api", alertRoutes);

// Start the server
app.listen(PORT, () => {
    console.log("Server is running on port 3000");
});

console.log('Username:', process.env.AFRICASTALKING_USERNAME);
console.log('API Key:', process.env.AFRICASTALKING_API_KEY);

