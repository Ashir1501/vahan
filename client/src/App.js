import React from 'react';
import logo from './logo.svg';
import './App.css';
import {Route, Routes, BrowserRouter} from "react-router-dom"
import Home from './pages/Home'
import Login from './pages/Login'
import Register from './pages/Register'
import BookingCar from './pages/BookingCar'
import Services from './pages/Services'
import Career from './pages/Career'
import AboutUs from './pages/AboutUs'
import CancellationRefundPolicy from './pages/Cancellation-Refund-Policy'
import PrivacyPolicy from './pages/Privacy-Policy'
import CorporateBooking from './pages/Corporate-Booking'
import BookingConfirmation from './pages/Booking-Confirmation'
import Payment from './pages/Payment'
import Blog from './pages/Blog'
import Termsandcondition from './pages/Terms-and-condition'

function App() {
  return (
    <div className="App">
      
      <BrowserRouter>

        <Routes>
          <Route path='/' exact Component={Home} />
          <Route path='/login' exact Component={Login} />
          <Route path='/register' exact Component={Register} />
          <Route path='/bookingcar' exact Component={BookingCar} />
          <Route path='/services' exact Component={Services} />
          <Route path='/career' exact Component={Career} />
          <Route path='/aboutus' exact Component={AboutUs} />
          <Route path='/cancellation-refund-policy' exact Component={CancellationRefundPolicy} />
          <Route path='/privacy-policy' exact Component={PrivacyPolicy} />
          <Route path='/corporate-booking' exact Component={CorporateBooking} />
          <Route path='/booking-confirmation' exact Component={BookingConfirmation} />
          <Route path='/terms-and-condition' exact Component={Termsandcondition} />
          <Route path='/payment' exact Component={Payment} />
          <Route path='/blogs' exact Component={Blog} />

        </Routes>     
      </BrowserRouter>

    </div>
  );
}

export default App;
