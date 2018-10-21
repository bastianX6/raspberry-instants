import firebase_admin
import json
import logging
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
from pathlib import Path

class FirebaseManager(object):

    def __init__(self, songsFolder, keysFolder):
        '''
        Constructor
        '''
        with open(keysFolder+'/gc_data.json', 'r') as f:
            self.firebaseData = json.load(f)


        self.credential = credentials.Certificate(keysFolder+'/gc_key.json')
        firebase_admin.initialize_app(self.credential, {
            'storageBucket': '{}.appspot.com'.format(self.firebaseData['cloud_storage']['bucket_name'])
        })
        self.db = firestore.client()
        self.bucket = storage.bucket()
        self.songsReference = self.db.collection(self.firebaseData['firestore']['collection_name'])
        self.songsFolder = songsFolder

    def getData(self):
        docs = self.songsReference.order_by(self.firebaseData['firestore']['field_name']).limit(1).get()
        for doc in docs:
            return doc.to_dict()

    def getSongsFiles(self):
        prefix = self.firebaseData['cloud_storage']['file_prefix']
        blobs = self.bucket.list_blobs(prefix = prefix)
        for blob in blobs:
            fileName = blob.name.replace(prefix, '')
            if len(fileName) == 0:
                continue

            localPath = self.songsFolder+u'/'+fileName
            logging.debug("fileName: %s", fileName)
            if not Path(localPath).exists():
                logging.warning("File %s doesn't exists. Downloading...", fileName)
                self.download_blob(blob.name, localPath)

    def download_blob(self, source_blob_name, destination_file_name):
        """Downloads a blob from the bucket."""
        blob = self.bucket.blob(source_blob_name)

        blob.download_to_filename(destination_file_name)
        logging.info('Sound %s downloaded to %s.', source_blob_name, destination_file_name)
