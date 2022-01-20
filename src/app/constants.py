from app.firebase_init import getFirestoreClient

client = getFirestoreClient()

# The station id should come from env..
station_ref = client.collection(u'stations').document(u'B1UNaOTznfzZXgxxUTnc')
