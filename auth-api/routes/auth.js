const express = require('express');
const router = express.Router();
const {
    registerUser,
    loginUser,
    updateUserProfile,
    resetPasswordRequest,
    resetPassword,
    getUserProfile
} = require('../controllers/authController');
const auth = require('../middleware/auth');

// Register route
router.post('/register', registerUser);

// Login route
router.post('/login', loginUser);

// Update profile route (protected)
router.put('/update-profile', auth, updateUserProfile);

// In auth.js routes file
router.post('/reset-password-request', resetPasswordRequest);


// Reset password route
router.post('/reset-password/:token', resetPassword);

// Get user profile route (protected)
router.get('/me', auth, getUserProfile);

module.exports = router;
