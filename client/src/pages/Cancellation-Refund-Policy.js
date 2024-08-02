import React from 'react'
import DefaultLayout from '../components/DefaultLayout'
import './Cancellation-Refund-Policy.css';

function cancellationrefundpolicy() {
  return (
    <DefaultLayout> 
      <main className="refund-policy-page">
        <h2>Refund Policy, Cancellation and Returns</h2>
        
        <section>
          <h3>Cancellation Policy</h3>
          <p>
            You may cancel the booking 24 hours prior to the time of journey, without any cancellation charges for all services. In case cancellation or shortening of the trip is requested within 24 hours of the pick-up time, the following rules will apply:
          </p>
          <ul>
            <li>
              <strong>Multi Day trip:</strong> The charge for the first day would be deducted from the total amount and a refund will be issued to the user.
            </li>
            <li>
              <strong>Single Day trip/ Airport transfer:</strong> No Refund will be issued to the user.
            </li>
            <li>
              <strong>Airport transfer:</strong> No Cancellation Charges if Cancelled at least 2 hours prior to the pickup time.
            </li>
          </ul>
        </section>

        <section>
          <h3>Refunds</h3>
          <p>
            If you are eligible for refunds based on the “Cancellation and Returns” policy above, then the refund will be remitted back to you in 5-7 working days. In case of any issues, write to us at <a href="mailto:vahancarrental@gmail.com">vahancarrental@gmail.com</a> or call us at <a href="tel:919137517508">+91 91375-17508</a>.
          </p>
        </section>
      </main>
    </DefaultLayout>
  )
}

export default cancellationrefundpolicy



