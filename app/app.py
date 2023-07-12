from flask import Flask, jsonify
import serverless_wsgi
import nostr_helper

app = Flask(__name__)

@app.route('/verify', methods=['GET'])
def verify_API():
    nostr_helper.verify_API()
    return jsonify(message="Success")

@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    return jsonify(message=f"You've hit the {path} path")

def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)
