const express = require('express');
const router = express.Router();
const { updateProfile, resetPassword } = require('../controllers/userController');
const auth = require('../middleware/auth');

router.put('/profile', auth, updateProfile);
router.post('/reset-password', resetPassword);

module.exports = router;
