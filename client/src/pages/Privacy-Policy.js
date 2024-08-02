import React from 'react';
import DefaultLayout from '../components/DefaultLayout';
import './Privacy-Policy.css';

const PrivacyPolicy = () => {
  return (
    <DefaultLayout>
      <div className="privacy-policy-page">
        <h1>Privacy Policy Page</h1>
        
        <p>
          This privacy policy sets out how Vahan Car Rentals uses and protects any information that you give Vahan Car Rentals when you use this website.
        </p>
        <p>
          Vahan Car Rentals is committed to ensuring that your privacy is protected. Should we ask you to provide certain information by which you can be identified when using this website, then you can be assured that it will only be used in accordance with this privacy statement.
        </p>
        <p>
          Vahan Car Rentals may change this policy from time to time by updating this page. You should check this page from time to time to ensure that you are happy with any changes. This policy is effective from 31st July 2006.
        </p>

        <h3>Information We Collect</h3>
        <p>We may collect the following information:</p>
        <ul>
          <li>Name and job title</li>
          <li>Contact information including email address</li>
          <li>Demographic information such as postcode, preferences, and interests</li>
          <li>Other information relevant to customer surveys and/or offers</li>
        </ul>
        <p>
          In addition to any protected information or other information that you choose to submit to us, we collect certain information whenever you visit or interact with the services (“usage information”). This usage information may include the browser that you are using, the URL that referred you to our services, all of the areas within our services that you visit, and the time of day, among other information. In addition, we collect your device identifier for your device. A device identifier is a number that is automatically assigned to your device used to access the services, and our computers identify your device by its device identifier. In case of booking via call center, Vahan Car Rentals may record calls for quality and training purposes.
        </p>

        <h3>Security</h3>
        <p>
          We are committed to ensuring that your information is secure. In order to prevent unauthorized access or disclosure we have put in place suitable physical, electronic and managerial procedures to safeguard and secure the information we collect online.
        </p>

        <h3>How We Use Cookies</h3>
        <p>
          A cookie is a small file which asks permission to be placed on your computer's hard drive. Once you agree, the file is added and the cookie helps analyze web traffic or lets you know when you visit a particular site. Cookies allow web applications to respond to you as an individual. The web application can tailor its operations to your needs, likes and dislikes by gathering and remembering information about your preferences.
        </p>

        <h3>Links to Other Websites</h3>
        <p>
          Our website may contain links to other websites of interest. However, once you have used these links to leave our site, you should note that we do not have any control over that other website. Therefore, we cannot be responsible for the protection and privacy of any information which you provide whilst visiting such sites and such sites are not governed by this privacy statement. You should exercise caution and look at the privacy statement applicable to the website in question.
        </p>

        <h3>Contacting Us</h3>
        <p>
          If there are any questions regarding this privacy policy you may contact us using the information on the Contact Us page.
        </p>

        <h3>Account Deletion</h3>
        <p>
          Account deletion can be done through Vahan Car Rentals App. Please follow the following steps:
        </p>
        <ol>
          <li>Go to Profile Section (Top right corner) and click on Edit Account</li>
          <li>Click on Delete Account Tab</li>
          <li>Answer 3 simple feedback questions</li>
        </ol>
        <p>
          After deletion, the user account will be completely removed from Vahan Car Rentals’s database including user details and booking history. There will be no communications from Vahan Car Rentals to the deleted users with regards to any offers or marketing campaigns. In case the user creates another account with the same credentials, the old booking data won’t be available since this account will be considered as a fresh sign-up.
        </p>
      </div>
    </DefaultLayout>
  );
}

export default PrivacyPolicy;
