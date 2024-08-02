import React from 'react'
import DefaultLayout from '../components/DefaultLayout'
import './Services.css';

function Services() {
  return (
    <DefaultLayout>
        <main className="services-page">
        <h2>Our Services</h2>
        
        <section>
          <h3>Outstation Oneway Drops</h3>
          <p>
            Convenient one-way trips to your destination without the hassle of return journeys. Enjoy a comfortable ride to your desired location with our reliable outstation one-way drop services.
          </p>
        </section>

        <section>
          <h3>Outstation Roundtrips</h3>
          <p>
            Plan your roundtrip journeys with ease and comfort. Our outstation roundtrip services ensure you have a smooth and enjoyable travel experience, both to and from your destination.
          </p>
        </section>

        <section>
          <h3>Hourly Local Rentals</h3>
          <p>
            Flexible hourly rentals for your local travel needs. Whether it's a quick trip to the market or a day-long business meeting, our hourly rental services provide you with the flexibility and convenience you need.
          </p>
        </section>

        <section>
          <h3>Airport Transfers</h3>
          <p>
            Hassle-free transfers to and from the airport. Our airport transfer services guarantee a timely and comfortable ride, ensuring you never miss a flight or have to wait long after landing.
          </p>
        </section>
      </main>
    </DefaultLayout>
  )
}

export default Services





