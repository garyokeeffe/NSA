from flask import Flask, jsonify
import serverless_wsgi
import nostr_helper

app = Flask(__name__)

@app.route('/')
def verify_API():
    nostr_helper.verify_API()
    return jsonify(message="Success")

def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)