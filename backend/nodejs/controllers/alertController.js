const { sendSMS } = require('../services/smsService'); // Import the service

// Controller to handle the alert logic
const handleAlert = async (req, res) => {
    const { message, phoneNumber } = req.body;

    try {
        // Send the SMS through the SMS service
        await sendSMS(message, phoneNumber);
        res.status(200).json({ success: true, message: "Alert sent successfully!" });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
};

module.exports = { handleAlert };
