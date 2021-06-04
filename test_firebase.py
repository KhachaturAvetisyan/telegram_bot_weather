import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# https://firebase.google.com/docs/firestore/quickstart#python

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# Добавляем что-то в базу данных
doc_ref = db.collection(u'user').document(u'817332557')
doc_ref.set({
    u'city': 'Erevan'
})

# Читаем базу данных
users_ref = db.collection(u'user')
docs = users_ref.stream()

for doc in docs:
    # print(f'{doc.id} => {doc.to_dict()}')
	print(doc.to_dict()['city'])