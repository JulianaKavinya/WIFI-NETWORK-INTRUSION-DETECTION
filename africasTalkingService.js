const axios = require('axios');

const africastalking = require('africastalking')({
    apiKey: process.env.AFRICASTALKING_API_KEY, // Make sure this is defined
    username: process.env.AFRICASTALKING_USERNAME // Make sure this is defined
});

const sendSms = async (mac, ip) => {
    try {
        console.log('Sending SMS with MAC:', mac, 'and IP:', ip);

        // Create form data in URL-encoded format
        const formData = new URLSearchParams();
        formData.append('username', USERNAME);
        formData.append('to', '+254758392102'); // Replace with recipient phone number
        formData.append('message', `New Device Detected! MAC: ${mac}, IP: ${ip}`);
        formData.append('bulkSMSMode', '1');

        // Make the POST request with URL-encoded data
        const response = await axios.post(
            'https://api.africastalking.com/version1/messaging',
            formData.toString(), // Pass formData as a string
            {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'apikey': API_KEY,
                },
            }
        );

        console.log('SMS sent successfully:', response.data);
        return response.data;
    } catch (error) {
        console.error('Failed to send SMS:', error.response ? error.response.data : error.message);
        throw error;
    }
};

module.exports = { sendSms };