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

@app.route('/notif', methods=['GET'])
def sendNotif():
    # Send to single device.
    from pyfcm import FCMNotification

    push_service = FCMNotification(api_key="AIzaSyDSyjypPVBRjd70Vi96cIYdL5uIww4tf_U")

    # OR initialize with proxies

    # proxy_dict = {
    #           "http"  : "http://127.0.0.1",
    #           "https" : "http://127.0.0.1",
    #         }
    # push_service = FCMNotification(api_key="<api-key>", proxy_dict=proxy_dict)

    # Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging

    registration_id = "AAAAG3qILFk:APA91bE-HPHUiOYk7CVyaH4Y0vzwxePISFUSYkuUAXfOIVgOtspuCFJ0Mw_l_1vOrugiQucPKj4vLLeinfCTpfm3KhMYo4CKuNc1JCdZHJX8WEUDvwoMPl_XKU0LbPjk8n8pxkceSnsW"
    message_title = "Credit added"
    message_body = "Hi, here are the news"
    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

    # # Send to multiple devices by passing a list of ids.
    # registration_ids = ["<device registration_id 1>", "<device registration_id 2>", ...]
    # message_title = "Uber update"
    # message_body = "Hope you're having fun this weekend, don't forget to check today's news"
    # result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)

    print (result)

@app.route('/client/<id_cl>/<id_cu>', methods=['GET'])
def add_client(id_cl,id_cu):
    # end = Client.child('END').get()
    # end = end +1
    # req = flask.request.json
    # res = Client.update({end:req})
    db.reference('client_db/'+str(id_cl)).push(id_cu)
    # res = Client. update(req)
    # return flask.jsonify({'id': res.key}), 201
    return "Success "

@app.route('/station/<id_tr>/<id_cu>', methods=['GET'])
def add_cup(id_tr,id_cu):
    # end = Client.child('END').get()
    # end = end +1
    # req = flask.request.json
    # res = Client.update({end:req})
    db.reference('trash_db/'+str(id_tr)).push(id_cu)
    # res = Client. update(req)
    # return flask.jsonify({'id': res.key}), 201
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
