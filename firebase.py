import firebase_admin
import json
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage

class FirebaseDatabse(object):

    def __init__(self):
        '''
        Constructor
        '''
        with open('Keys/gc_data.json', 'r') as f:
            self.firebaseData = json.load(f)


        self.credential = credentials.Certificate('Keys/gc_key.json')
        firebase_admin.initialize_app(self.credential, {
            'storageBucket': '{}.appspot.com'.format(self.firebaseData['cloud_storage']['bucket_name'])
        })
        self.db = firestore.client()
        self.bucket = storage.bucket() 
        self.songsReference = self.db.collection(self.firebaseData['firestore']['collection_name'])

    def getData(self):
        docs = self.songsReference.order_by(self.firebaseData['firestore']['field_name']).limit(1).get()
        for doc in docs:
            return doc.to_dict()

    def getSongsFiles(self):
        pass
    