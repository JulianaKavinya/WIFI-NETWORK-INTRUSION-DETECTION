// services/smsService.js

const AfricasTalking = require('africastalking');

// Initialize AfricasTalking with your credentials
const africasTalking = AfricasTalking({
    apiKey: process.env.AFRICASTALKING_API_KEY,
    username: process.env.AFRICASTALKING_USERNAME,
});

const sms = africasTalking.SMS;

// Function to send SMS
const sendSMS = async (message, phoneNumber) => {
    try {
        const response = await sms.send({ to: [phoneNumber], message });
        return response;
    } catch (error) {
        throw new Error(error.message);
    }
};

module.exports = { sendSMS };
