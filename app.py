from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import db, credentials
import flask

app = Flask(__name__)

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred,options={
    'databaseURL': 'https://socup-27717.firebaseio.com'
})
idx=0

# firebase_admin.initialize_app(options={
#     'databaseURL': 'https://socup-27717.firebaseio.com'
# })
Client = db.reference('client_db')
Trash = db.reference('trash_db')

# @app.route('/notif', methods=['GET'])
def sendNotif():
    # Send to single device.
    from pyfcm import FCMNotification

    push_service = FCMNotification(api_key="AAAAG3qILFk:APA91bE-HPHUiOYk7CVyaH4Y0vzwxePISFUSYkuUAXfOIVgOtspuCFJ0Mw_l_1vOrugiQucPKj4vLLeinfCTpfm3KhMYo4CKuNc1JCdZHJX8WEUDvwoMPl_XKU0LbPjk8n8pxkceSnsW")

    registration_id = "dag7_IRL9bU:APA91bEZr7tCtEsRo_6TCC6WM8b9-dHGVyHFGZ8W8A50weXaI_cEGmuYqHLHsVKXWilvd1uqbnJD08UwY99j5EC-KSvh_GWflCYXgP9stfWeVquhLrWgBlYuDD2z8DQ2HOk-iQiukGUO" #"dQFOpaQ57L8:APA91bHKGbAz0mV5KMNsbcbfHwIy8PoZgPL9ad19g_KepnDcSw4rr9mNyYWUw9Mkj4hcguP7ekI-dTjUK8nydzxSmwdcWhgJSwgUTZdMJMvdC4_nLhWg3o6BjE4YGpk1gj39ZZHKb6fu"
    message_title = "Cup returned"
    message_body = "Thanks for your contribution"
    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

@app.route('/client', methods=['POST'])
def add_client():
    data = request.get_json()
    id_cl = data["id_cl"]
    id_cu = data["id_cu"]
    # end = Client.child('END').get()
    # end = end +1
    # req = flask.request.json
    # res = Client.update({end:req})
    db.reference('client_db/'+str(id_cl)).push(id_cu)
    # res = Client. update(req)
    # return flask.jsonify({'id': res.key}), 201
    return "Success "

@app.route('/station', methods=['POST'])
def add_cup():
    data = request.get_json()
    id_tr = data["id_tr"]
    id_cu = data["id_cu"]
    # end = Client.child('END').get()
    # end = end +1
    # req = flask.request.json
    # res = Client.update({end:req})
    db.reference('trash_db/'+str(id_tr)).push(id_cu)
    # res = Client. update(req)
    # return flask.jsonify({'id': res.key}), 201
    sendNotif()
    return "Success "

@app.route('/station/<id>/json', methods=['GET'])
def get_cups(id):
    info = db.reference('trash_db/' + str(id)).get()
    if not info:
        flask.abort(404)
    return flask.jsonify(info)

@app.route('/station/<id>', methods=['GET'])
def get_num_cups(id):
    info = db.reference('trash_db/' + str(id)).get()
    if not info:
        return "0"
    return str(len(info))

@app.route('/client/<id>/json', methods=["GET"])
def get_client(id):
    info = db.reference('client_db/' + str(id)).get()
    if not info:
        flask.abort(404)
    return flask.jsonify(info)

@app.route('/client/<id>', methods=["GET"])
def get_num_client(id):
    info = db.reference('client_db/' + str(id)).get()
    if not info:
        return "0"
    return str(len(info))

@app.route('/')
def hello_world():
    return 'Welcome!'

if __name__ == '__main__':
    app.run()
