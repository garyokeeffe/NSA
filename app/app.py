from flask import Flask, jsonify, request
import serverless_wsgi
import nostr_helper

app = Flask(__name__)


@app.route('/verify', methods=['GET'])
def verify_API():
    nostr_helper.verify_API()
    return jsonify(message="Success")

@app.route('/fetch_notes', methods=['POST'])
def fetch_text_notes():
    try:
        request_data = request.get_json()
        if request_data['relays']:
            relays = request_data['relays']
        if request_data['authors']:
            authors = request_data['authors']
        else:
            authors = []
        return jsonify(nostr_helper.fetch_text_notes(authors, relays))
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred'}), 500
    
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    return jsonify(message=f"You've hit the {path} path")

def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)
