const functions = require('firebase-functions');
const admin = require('firebase-admin');
const express = require('express');
const app = express();

admin.initializeApp(functions.config().firebase);

var db = admin.firestore();

app.post('/song', (req, res) => {

    var Validator = require('jsonschema').Validator;
    var v = new Validator();
    var songSchema = {
        "songCode": {"type": "string"},
        "description": {"type": "string"},
        "songName": {"type": "string"},
        "public": {"type": "boolean"},
    }
    var song = req.body;
    if(v.validate(req.body, songSchema).valid) {
        db.collection("songs2").add(req.body)
        .then( ref => { 
            res.status(201).json("Song added successfully");
        }).catch( err => {
            res.status(400).json("Error: "+err);
        });
    } else {
        res.status(400).json("Invalid JSON");
    }

});

exports.botonera = functions.https.onRequest(app);
