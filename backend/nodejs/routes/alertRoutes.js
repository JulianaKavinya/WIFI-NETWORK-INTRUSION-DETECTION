
const express = require('express');
const router = express.Router();
const { sendSMS } = require('../services/africastalkingService');  // Import sendSMS from the service
const { handleAlert } = require('../controllers/alertController'); // Use the controller function

// Route to handle alerts (SMS sending logic)
router.post('/', handleAlert); // Matches POST requests to '/alerts'
router.post('/alerts', async (req, res) => {
    const { message, phoneNumber } = req.body;
    if (!message || !phoneNumber) {
        return res.status(400).json({ success: false, error: 'Message and phoneNumber are required.' });
    }

    try {
        // Call the sendSMS function from africastalkingService.js
        const response = await sendSMS(message, phoneNumber);

        // Send success response if SMS is sent successfully
        res.status(200).json({ success: true, message: 'SMS sent successfully', response });
    } catch (error) {
        // Send error response in case of failure
        console.error('Error sending SMS:', error);
        res.status(500).json({ success: false, error: error.message || 'Internal Server Error' });
    }
});

module.exports = router;




