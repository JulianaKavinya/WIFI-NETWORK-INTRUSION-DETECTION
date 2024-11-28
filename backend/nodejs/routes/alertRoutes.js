const express = require('express');
const router = express.Router();
const { sendSMS } = require('../services/africasTalkingService');

router.post('/alerts', async (req, res) => {
    const { message, phoneNumber } = req.body;
    try {
        await sendSMS(message, phoneNumber);
        res.status(200).json({ success: true });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

module.exports = router;
