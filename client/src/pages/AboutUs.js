import React from 'react'
import DefaultLayout from '../components/DefaultLayout'
import './AboutUs.css';

function aboutus() {
  return (
    <DefaultLayout>
        <main className="aboutus">
        
        
        <h2>Vahan Car Rental Service</h2>
        
        <section>
          <p>
          Vahan is India's premier chauffeur driven car rental service. Since our inception in 2006, we have constantly strived to offer reliable, safe, and affordable cabs. Our presence in over 2000 cities across the country uniquely positions us as India's largest geographical network of cab services. Our services include Outstation Oneway drops, Outstation Roundtrips, Hourly Local Rentals, and Airport Transfers.
          </p>
        </section>

        <section>
          <p>
            That said, we don't want to be remembered as just another Car Rental company. Our mission is to 'Make every Indian fall in love with Road Travel'. Roaming on serpentine roads of India, where ancient mountains whisper tales of time and saree-clad silhouettes pirouette in marigold sunsets. The air vibrates with manifold dialects, harmonized by sweet symphonies of hymns. Vendors sell spicy chaat, bazaars burst with kaleidoscopic trinkets, while incense from far-off temples paints the journey in divine hues. What better way to experience these sights, sounds, smells and tastes than in a chauffeur-driven car?
          </p>
        </section>

        <section>
          <h3>Why drive, when you can have Vahan?</h3>
        </section>
      </main>
    </DefaultLayout>
  )
}

export default aboutus


