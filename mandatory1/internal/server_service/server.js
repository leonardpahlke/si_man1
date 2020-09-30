const express = require('express');
const csv = require('csv-parser');
const fs = require('fs');

var app = express();
var results = [];

app.get('/get-people', (req, res) => {
    fs.createReadStream('people.csv')
        .pipe(csv())
        .on('data', (data) => results.push(data))
        .on('end', () => {
        res.status(200).send(results)
        });
});


app.listen(8000, (err) => {
    if(err){
        console.log(err);
        return;
    }
    console.log('Server running on port 8000');
})