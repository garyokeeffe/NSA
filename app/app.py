from flask import Flask, jsonify, request
import serverless_wsgi
import nostr_helper

app = Flask(__name__)


@app.route('/v0/verify', methods=['POST'])
def verify_API():
    try:
        request_data = request.get_json()
        relays = nostr_helper.find_request_relay(request_data)
        private_key = request_data.get('private_key')
        if not private_key:
            return jsonify({'error': 'You need to include an nsec private key in your request.'}), 500
        return jsonify(nostr_helper.send_text_note(text = "Running Nostr Serverless API", private_key = private_key, relays = relays))
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/v0/fetch/notes', methods=['POST'])
def fetch_text_notes():
    try:
        request_data = request.get_json()
        event_filter = nostr_helper.generate_fetch_note_filter(request_data)
        relays = nostr_helper.find_request_relay(request_data)
        return jsonify(nostr_helper.fetch_text_notes(event_filter, relays))
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/v0/send/note', methods=['POST'])
def send_text_note():
    try:
        request_data = request.get_json()
        relays = nostr_helper.find_request_relay(request_data)
        text = request_data.get('text')
        if not text:
            return jsonify({'error': 'You need to include text in your request.'}), 500
        private_key = request_data.get('private_key')
        if not private_key:
            return jsonify({'error': 'You need to include an nsec private key in your request.'}), 500
        return jsonify(nostr_helper.send_text_note(text, private_key, relays))
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route('/v0/send/dm', methods=['POST'])
def send_dm():
    try:
        request_data = request.get_json()
        text = request_data.get('text')
        if not text:
            return jsonify({'error': 'You need to include text in your request.'}), 500
        private_key = request_data.get('sender_private_key')
        if not private_key:
            return jsonify({'error': 'You need to include an nsec sender private key in your request.'}), 500
        public_key = request_data.get('recipient_public_key')
        if not public_key:
            return jsonify({'error': 'You need to include the recipients public key in your request.'}), 500
        relays = nostr_helper.find_request_relay(request_data)
        return jsonify(nostr_helper.send_dm(text, private_key, public_key, relays))
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred'}), 500


def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)
