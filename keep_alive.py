from flask import Flask, Response
from threading import Thread
from replit import db
import json

app = Flask('')
app.config['JSON_AS_ASCII'] = False


# Defines a class for each message in the db
class Message:
    id = 0
    message = ""

    def __init__(self, id, message):
        self.id = id
        self.message = message


@app.route('/')
def home():
    return "Hello. I am alive!"


@app.route('/stats')
def stats():
    if "encouragements" in db.keys():
        stats = {
            'total_messages': len(db["encouragements"]),
            'total_actions': len(db["actions"])
        }
        statsJson = json.dumps(stats,
                               indent=4,
                               sort_keys=True,
                               ensure_ascii=False)
        return Response(statsJson,
                        200,
                        content_type="application/json; charset=utf-8")
    else:
        return str(0)


# Displays a list of all messages
@app.route('/bot/messages', methods=['GET'])
def messages():
    response = Response(messagesToJson(),
                        200,
                        content_type="application/json; charset=utf-8")
    return response


@app.route('/bot/actions', methods=['GET'])
def actions():
    response = Response(db["actions"],
                        200,
                        content_type="application/json; charset=utf-8")
    return response


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()


def messagesToObject():
    if "encouragements" in db.keys():
        i = 0
        encouragements = []
        for key in db["encouragements"]:
            encouragements.append(Message(i, key))
            i += 1
        return encouragements


# Retrieves messages from the db
def messagesToJson():
    if "encouragements" in db.keys():
        i = 0
        encouragements = []
        for key in messagesToObject():
            encouragements.append(key.__dict__)
            i += 1
        return json.dumps(encouragements,
                          indent=4,
                          sort_keys=True,
                          ensure_ascii=False)
    return ''
