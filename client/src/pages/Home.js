import React, { useState } from 'react';
import DefaultLayout from '../components/DefaultLayout';
import './Home.css';


const Home = () => {
  

  return (
    <DefaultLayout>
      
        <div className="car-rental-booking">
          <CarRentalBooking />
          <h1>Maps</h1>
          <div className="container-fluid">
        <div className="map-responsive">
          <iframe
            src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3769.433043393542!2d72.8749373!3d19.132512600000002!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3be7b79931d7a633%3A0xcd628b2e25bf2dd3!2sVAHAN%20CAR%20RENTALS!5e0!3m2!1sen!2sin!4v1694622621762!5m2!1sen!2sin"
            width="100%"
            height="480"
            style={{ border: 0 }}
            allowFullScreen=""
            loading="lazy"
            referrerPolicy="no-referrer-when-downgrade"
            title="Google Maps"
          ></iframe>
        </div>
      </div>
        </div>
    
    </DefaultLayout>
  );
};

const CarRentalBooking = () => {
  const [activeTab, setActiveTab] = useState('oneway');

  const renderFormContent = () => {
    switch (activeTab) {
      case 'oneway':
        return (
          <div>
            <label>Pick-up Location:</label>
            <input type="text" placeholder="Enter pick-up location" />
            <label>Drop-off Location:</label>
            <input type="text" placeholder="Enter drop-off location" />
            <label>Pick-up Date:</label>
            <input type="date" />
          </div>
        );
      case 'roundtrip':
        return (
          <div>
            <label>Pick-up Location:</label>
            <input type="text" placeholder="Enter pick-up location" />
            <label>Drop-off Location:</label>
            <input type="text" placeholder="Enter drop-off location" />
            <label>Pick-up Date:</label>
            <input type="date" />
            <label>Return Date:</label>
            <input type="date" />
          </div>
        );
      case 'local':
        return (
          <div>
            <label>Pick-up Location:</label>
            <input type="text" placeholder="Enter pick-up location" />
            <label>Pick-up Date:</label>
            <input type="date" />
            <label>Pick-up Time:</label>
            <input type="time" />
            <label>Duration (in hours):</label>
            <input type="number" placeholder="Enter duration" />
          </div>
        );
      case 'airport':
        return (
          <div>
            <label>Pick-up Location:</label>
            <input type="text" placeholder="Enter pick-up location" />
            <label>Drop-off Location (Airport):</label>
            <input type="text" placeholder="Enter airport" />
            <label>Pick-up Date:</label>
            <input type="date" />
            <label>Pick-up Time:</label>
            <input type="time" />
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="car-rental-booking">
      <div className="tabs">
        <button onClick={() => setActiveTab('oneway')} className={activeTab === 'oneway' ? 'active' : ''}>One Way</button>
        <button onClick={() => setActiveTab('roundtrip')} className={activeTab === 'roundtrip' ? 'active' : ''}>Round Trip</button>
        <button onClick={() => setActiveTab('local')} className={activeTab === 'local' ? 'active' : ''}>Local</button>
        <button onClick={() => setActiveTab('airport')} className={activeTab === 'airport' ? 'active' : ''}>Airport</button>
      </div>
      <form className="form-content">
        {renderFormContent()}
        <button type="submit">Book Now</button>
      </form>
    </div>
  );
};



export default Home;
