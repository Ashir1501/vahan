// src/DefaultLayout.js
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './DefaultLayout.css'; // Ensure you have this CSS file for styles
import { FaUserCircle, FaBars } from 'react-icons/fa'; // Import FaBars for hamburger icon

function DefaultLayout(props) {
  const [showMenu, setShowMenu] = useState(false);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <nav className="navbar">
        <div className="navbar-logo">
          <img src="../images/Ca.png" alt="Logo" /> {/* Update with your logo path */}
        </div>
        {/* Use onClick event to toggle the showMenu state */}
        <FaBars className="navbar-hamburger" onClick={() => setShowMenu(!showMenu)} size={30} />
        <ul className={`navbar-list ${showMenu ? 'active' : ''}`}>
          <li><Link to="/">Home</Link></li>
          <li><Link to="/services">Services</Link></li>
          <li><Link to="/career">Career</Link></li>
          <li><Link to="/blogs">Blogs</Link></li>
          <li><Link to="/aboutus">About Us</Link></li>
          <li class="login-item">
        <a href="/login"><img src="login-icon.png" alt="Login"></img></a>
      </li>
         
          
        </ul>
        <div className="navbar-login">
          <FaUserCircle size={30} />
          <Link to="/login">Login</Link>
        </div>
      </nav>

      <div className="content" style={{ flex: 1 }}>
        {props.children}
      </div>
      <footer style={{ backgroundColor: 'aqua', color: 'black' }}>
        <br />
        <div className="container">
          <div className="row">
            <div className="col-lg-3">
              <h4 id="About_usH4">About Us</h4>
              <p>We understand that businesses require reliable transportation solutions. Vahan Car Rentals offers corporate plans that provide cost-effective and efficient mobility for your employees. We partner with companies to streamline their transportation needs, saving them time and money.</p>
            </div>
            <div className="col-lg-3">
              <h4>COMPANY INFO</h4>
              <ul className="list-unstyled">
                <li><a href="/services">SERVICES</a></li>
                <li><a href="/career">CAREER</a></li>
                <li><a href="/aboutus">ABOUT US</a></li>
                <li><a href="/blogs">BLOGS</a></li>
                
              </ul>
            </div>
            <div className="col-lg-3">
              <h4>Useful Link</h4>
              <ul className="list-unstyled">
                <li><a href="/cancellation-refund-policy">REFUND POLICY</a></li>
                <li><a href="/terms-and-condition">TERMS & CONDITION</a></li>
                <li><a href="/privacy-policy">PRIVACY POLICY</a></li>
                <li><a href="/corporate-booking">CORPORATE BOOKING</a></li>
              </ul>
            </div>
            <div className="col-lg-3">
              <h4>Newsletter</h4>
              <p>Enter your email address below:</p>
              <form action="">
                <div className="input-group">
                  <input type="email" name="" id="" className="form-control" />
                  <div className="input-group-append">
                    <button className="btn btn-secondary">Subscribe</button>
                  </div>
                </div>
                <br />
                <h4>Social Media</h4>
                <a href="https://www.facebook.com/profile.php?id=100091438371040">
                  <svg className="social-link-icon" width="30px" fill="#111" height="30px" viewBox="0 0 24 24">
                    <path d="M12 0C9.813 0 7.8.533 5.96 1.6A11.793 11.793 0 0 0 1.6 5.96C.533 7.8 0 9.813 0 12s.533 4.2 1.6 6.04a11.793 11.793 0 0 0 4.36 4.36C7.8 23.467 9.813 24 12 24s4.2-.533 6.04-1.6a11.793 11.793 0 0 0 4.36-4.36C23.467 16.2 24 14.187 24 12s-.533-4.2-1.6-6.04a11.793 11.793 0 0 0-4.36-4.36C16.2.533 14.187 0 12 0zm3.12 12h-2v7.2H10.4V12H8.64V9.52h1.76V8c0-1.12.187-1.92.56-2.4.427-.587 1.2-.88 2.32-.88h2V7.2h-1.2c-.427 0-.693.067-.8.2-.107.133-.16.387-.16.76v1.2h2.16L15.12 12z" />
                  </svg>
                </a>
                <a href="https://www.instagram.com/vahancarrentals/">
                  <svg className="social-link-icon" width="30px" fill="#111" height="30px" viewBox="0 0 24 24">
                    <path d="M16 12.48a4.723 4.723 0 0 1-.56 1.48 3.93 3.93 0 0 1-1.04 1.16 3.428 3.428 0 0 1-1.92.68 3.628 3.628 0 0 1-1.96-.48 3.414 3.414 0 0 1-1.4-1.48c-.48-.96-.587-1.973-.32-3.04H7.68l.08 5.52c0 .107.04.213.12.32.08.107.173.16.28.16h8.32c.107 0 .213-.053.32-.16.107-.107.16-.213.16-.32V10.8h-1.12c.16.533.213 1.093.16 1.68zm-3.68 2c.64 0 1.2-.24 1.68-.72s.72-1.053.72-1.72a2.56 2.56 0 0 0-.68-1.76c-.453-.507-1.013-.76-1.68-.76s-1.24.24-1.72.72-.72 1.053-.72 1.72.227 1.253.68 1.76c.453.507 1 .76 1.64.76h.08zm4.16-7.6h-1.12c-.107 0-.213.053-.32.16-.107.107-.16.213-.16.32v1.36c.107.213.267.32.48.32h1.12c.16 0 .28-.053.36-.16a.532.532 0 0 0 .12-.32v-1.2c0-.107-.053-.213-.16-.32-.107-.107-.213-.16-.32-.16zM12 0C9.813 0 7.8.533 5.96 1.6A11.793 11.793 0 0 0 1.6 5.96C.533 7.8 0 9.813 0 12s.533 4.2 1.6 6.04a11.793 11.793 0 0 0 4.36 4.36C7.8 23.467 9.813 24 12 24s4.2-.533 6.04-1.6a11.793 11.793 0 0 0 4.36-4.36C23.467 16.2 24 14.187 24 12s-.533-4.2-1.6-6.04a11.793 11.793 0 0 0-4.36-4.36C16.2.533 14.187 0 12 0zm6.24 16.88l-.08.08v.08a.926.926 0 0 1-.28.68 1.3 1.3 0 0 1-.68.36H7.52a.871.871 0 0 1-.68-.32 1.536 1.536 0 0 1-.36-.72l-.08-.16.08-9.84c0-.267.093-.507.28-.72.187-.213.413-.347.68-.4h9.68a1.3 1.3 0 0 1 .68.36 1.3 1.3 0 0 1 .36.68l.08 9.92z" />
                  </svg>
                </a>
              </form>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default DefaultLayout;
