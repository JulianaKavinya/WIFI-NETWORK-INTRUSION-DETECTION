// services/smsService.js
const express = require('express');
const AfricasTalking = require('africastalking');
const app = express();
const bodyParser = require('body-parser');

// Initialize AfricasTalking
const AfricasTalking = require('africastalking')({
    apiKey: process.env.AFRICASTALKING_API_KEY,
    username: process.env.AFRICASTALKING_USERNAME,
});
const sms = AfricasTalking.SMS;

app.use(bodyParser.json());  // Middleware to parse JSON body

// Send SMS function
const sendSMS = async (message, phoneNumber) => {
    return await sms.send({ to: [phoneNumber], message });
};

// API route to trigger sending an SMS
app.post('/send-sms', async (req, res) => {
    const { message, phoneNumber } = req.body;
    
    try {
        const response = await sendSMS(message, phoneNumber);
        res.status(200).json({ message: 'SMS sent successfully', response });
    } catch (error) {
        res.status(500).json({ message: 'Error sending SMS', error: error.message });
    }
});

// Start the server
const port = process.env.PORT || 3001;
app.listen(port, () => {
    console.log(`SMS service is running on port ${port}`);
});
