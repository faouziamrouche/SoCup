from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import db, credentials
import flask

app = Flask(__name__)

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred,options={
    'databaseURL': '<databaseURL>'
})
idx=0

Client = db.reference('client_db')
Trash = db.reference('trash_db')

def sendNotif():
    # Send to single device.
    from pyfcm import FCMNotification

    push_service = FCMNotification(api_key="<ApiKey>")

    registration_id = "<DeviceRegistrationId>"
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
