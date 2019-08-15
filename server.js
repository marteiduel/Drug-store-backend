require('dotenv').config();
const express = require('express'); //needed to launch server
const cors = require('cors'); //needed to disable sendgrid security
const sgMail = require('@sendgrid/mail'); //sendgrid library to send emails 

const PORT = process.env.PORT || 5000


const app = express(); //alias from the express function

//sendgrid api key
sgMail.setApiKey(process.env.REACT_APP_API);

app.use(cors()); //utilize Cors so the browser doesn't restrict data, without it Sendgrid will not send!

// Welcome page of the express server: 
app.get('/', (req, res) => {
    res.send("Welcome to the Sendgrid Emailing Server using node/express"); 
});

app.get('/send-email', (req,res) => {
    
    //Get Variables from query string in the search bar
    const { sender, topic, text, name, type } = req.query; 

    //Sendgrid Data Requirements
        const msg = type === 'SENDING'? {
        to: process.env.REACT_APP_EMAIL, 
        from: sender,
        subject: `${name} wants to know about: ${topic}`,
        text: text }:{
            to: sender, 
            from: 'info@avnsmotors.com',
            subject: `Re: ${topic}`,
            text: 'Thank you for contacting us. We will contact you as soon as possible.'
        };
   
    //Send Email
    sgMail.send(msg)
    .then((msg) => console.log('SENT'));
});

// to access server run 'nodemon index.js' then click here: http://localhost:4000/
app.listen(PORT, () => console.log("Running on Port 5000")); 