import React, { useState } from 'react';
import './Login.css';

const Login = () => {
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [otp, setOtp] = useState('');
  const [isEmailLogin, setIsEmailLogin] = useState(true);

  const handleEmailChange = (e) => setEmail(e.target.value);
  const handlePhoneChange = (e) => setPhone(e.target.value);
  const handleOtpChange = (e) => setOtp(e.target.value);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (isEmailLogin) {
      // Handle email login with OTP
      console.log(`Email: ${email}, OTP: ${otp}`);
    } else {
      // Handle phone login with OTP
      console.log(`Phone: ${phone}, OTP: ${otp}`);
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <h2>Login</h2>
        <div className="toggle-login">
          <button
            className={isEmailLogin ? 'active' : ''}
            onClick={() => setIsEmailLogin(true)}
          >
            Login with Email
          </button>
          <button
            className={!isEmailLogin ? 'active' : ''}
            onClick={() => setIsEmailLogin(false)}
          >
            Login with Phone
          </button>
        </div>
        <form onSubmit={handleSubmit} className="login-form">
          {isEmailLogin ? (
            <input
              type="email"
              value={email}
              onChange={handleEmailChange}
              placeholder="Enter your email"
              required
            />
          ) : (
            <input
              type="tel"
              value={phone}
              onChange={handlePhoneChange}
              placeholder="Enter your phone number"
              required
            />
          )}
          <input
            type="text"
            value={otp}
            onChange={handleOtpChange}
            placeholder="Enter OTP"
            required
          />
          <button type="submit">Login</button>
        </form>
        <div className="register-link">
          <a href="/register">Register Now / Sign Up Now</a>
        </div>
      </div>
    </div>
  );
};

export default Login;
