from flask import Flask, jsonify, request
import serverless_wsgi
import nostr_helper

app = Flask(__name__)


@app.route('/verify', methods=['POST'])
def verify_API():
    try:
        request_data = request.get_json()
        if request_data['relays']:
            relays = request_data['relays']
        if request_data['private_key']:
            private_key = request_data['private_key']
        else:
            return jsonify({'error': 'You need to include an nsec private key in your request.'}), 500
        return jsonify(nostr_helper.send_text_note(text = "Running Nostr Serverless API", private_key = private_key, relays = relays))
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    return jsonify(message=f"You've hit the {path} path")

@app.route('/v0/fetch/notes', methods=['POST'])
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

@app.route('/v0/send/note', methods=['POST'])
def send_text_note():
    try:
        request_data = request.get_json()
        if request_data['relays']:
            relays = request_data['relays']
        if request_data['text']:
            text = request_data['text']
        else:
            return jsonify({'error': 'You need to include text in your request.'}), 500
        if request_data['private_key']:
            private_key = request_data['private_key']
        else:
            return jsonify({'error': 'You need to include an nsec private key in your request.'}), 500
        return jsonify(nostr_helper.send_text_note(text, private_key, relays))
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    return jsonify(message=f"You've hit the {path} path")

def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)
