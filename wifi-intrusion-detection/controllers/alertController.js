const africasTalkingService = require('../services/africasTalkingService');

exports.sendAlert = async (req, res) => {
    const { mac_address, ip_address } = req.body;
    try {
        const response = await africasTalkingService.sendSms(mac_address, ip_address);
        res.status(200).json({ message: 'Alert sent successfully', response });
    } catch (error) {
        res.status(500).json({ message: 'Failed to send alert', error });
    }
};
