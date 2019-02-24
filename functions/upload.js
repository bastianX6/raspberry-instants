const functions = require('firebase-functions');
const admin = require('firebase-admin');
const express = require('express');
const app = express();
const { fileParser } = require('express-multipart-file-parser');

// Configuration
app.use(fileParser({
    rawBodyOptions: {
      limit: '1mb',
    },
    busboyOptions: {
      limits: {
        fields: 1
      }
    },
  }));

// WIP
app.post('/song/upload', (req, res) => {
    var file = req.files[0];
    if(!file) {
        return res.status(400).json("Error: Not file");
    }
    uploadToStorage(file)
    .then((success) => {
        res.status(201).send({
          status: 'success'
        });
    }).catch((error) => {
        console.log("Upload error: "+error);
        return res.status(400).json("Error in file upload");
    });

});


const uploadToStorage = (file) => {
    let prom = new Promise((resolve, reject) => {
      if (!file) {
        reject('No image file');
      }
      const {
        fieldname,
        originalname,
        encoding,
        mimetype,
        buffer,
      } = file;
      const bucket = admin.storage().bucket("raspberry-instants");
      console.log("bucket: "+JSON.stringify(bucket));
      let fileUpload = bucket.file("Songs/"+originalname);
  
      const blobStream = fileUpload.createWriteStream({
        metadata: {
          contentType: mimetype
        }
      });
  
      blobStream.on('error', (error) => {
          console.log("Error in upload: "+JSON.stringify(error));
        reject('Something is wrong! Unable to upload at the moment.');
      });
  
      blobStream.on('finish', () => {
        // The public URL can be used to directly access the file via HTTP.
        const url = format(`https://storage.googleapis.com/${bucket.name}/${fileUpload.name}`);
        resolve(url);
      });
  
      blobStream.end(file.buffer);
    });
    return prom;
  }

  exports.botonera2 = functions.https.onRequest(app);