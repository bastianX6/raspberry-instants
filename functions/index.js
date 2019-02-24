const functions = require('firebase-functions');
const admin = require('firebase-admin');
const express = require('express');
const app = express();

admin.initializeApp(functions.config().firebase);

var db = admin.firestore();

app.post('/song/add', (req, res) => {
    var Validator = require('jsonschema').Validator;
    var v = new Validator();
    var songSchema = require("./schemas/songSchema.json");
    var jsonIsValid = v.validate(req.body, songSchema).valid;
    if(!jsonIsValid) {
        return res.status(400).json("Invalid JSON");
    }
    var song = req.body;
    db.collection("songs2").add(req.body)
    .then( ref => {
        return res.status(201).json("Song added successfully");
    }).catch( err => {
        return res.status(400).json("Error: "+err);
    });
});

app.get('/song/list', (req, res) => {
    db.collection("songs2").where("public", "==", true).get()
    .then( snapshot => {
        var docData = snapshot.docs.map( doc => {
            return doc.data();
        })
        return res.status(200).json({"songs": docData});
    }).catch(err => {
        return res.status(400).json("Error getting documents: "+err);
    });
});

exports.botonera = functions.https.onRequest(app);
