const express = require('express');
var EsbImplementation = require('./esb');
const axios = require('axios');

let app = express();
app.use(express.json());

app.get('/', (req, res) => {
    res.status(200).send({message: "all is good"});
});

app.post('/trigger-esb', async (req, res) => {
    data = req.body;
    let esb = new EsbImplementation(data.name, "client", "someId");
    let response = await axios.get('http://localhost:8000/get-people');

    esb.configureEsb();

    response.data.forEach(element => {
        esb.sendMessage(element, element.Gender);
    });
    res.status(200).send("Done");
});

app.listen(8080, (err) => {
    if (err) {
        console.log("Unable to listen...");
        return;
    }
    console.log("Listening on 8080...");
});