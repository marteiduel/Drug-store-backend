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
    const { patientemail, name } = req.query; 

    //Sendgrid Data Requirements
        const msg = {
        to: patientemail, 
        from: process.env.REACT_APP_EMAIL,
        subject: 'GlucoBasal Assistance Program',
        text: `Dear ${name}
        Congratulations! You are eligible for the GlucoBasal Assistance Program! 
        This will allow you to receive up to a 30 day supply of your GlucoBasal insulin at a participating pharmacy. 
        Please use this email as an electronic proof of coverage or feel free to print a copy of this email as proof of coverage as no physical proof of coverage will be sent to you. 
        Here is the information that the participating pharmacy will need:
        BIN: 980980
        PCN: ABC123
        GROUP: GlucoBasal999
        ID: {SWE000000001}
        If you have any questions, please feel free to contact us.

        To Your Health,
        The GlucoBasal Foundation
        120 Sugarbowl Avenue
        Sucrose, LA 01234-5678
        ` }
   
    //Send Email
    sgMail.send(msg)
    .then((msg) => console.log('SENT'));
});

// to access server run 'nodemon index.js' then click here: http://localhost:5000/
app.listen(PORT, () => console.log("Running on Port 5000"));