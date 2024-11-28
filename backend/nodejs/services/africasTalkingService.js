const AfricasTalking = require('africastalking')({
    apiKey: process.env.AFRICASTALKING_API_KEY,
    username: process.env.AFRICASTALKING_USERNAME,
});

const sms = AfricasTalking.SMS;

const sendSMS = async (message, phoneNumber) => {
    return await sms.send({ to: [phoneNumber], message });
};

module.exports = { sendSMS };
