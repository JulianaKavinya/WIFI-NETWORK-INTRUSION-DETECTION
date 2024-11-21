const express = require('express');
const router = express.Router();
const alertController = require('../controllers/alertController');

// Route to send SMS alert
router.post('/send_alert', alertController.sendAlert);

module.exports = router;


