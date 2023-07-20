import time
import os
from nostr.relay_manager import RelayManager
from nostr.key import PrivateKey
from nostr.event import EncryptedDirectMessage,Event, EventKind
from nostr.delegation import Delegation
import json
import ssl
import time
from nostr.key import PublicKey
from nostr.filter import Filter, Filters
from nostr.message_type import ClientMessageType
import uuid

def convert_to_hex(input_str):
    if input_str.startswith('npub'):
        input_str = PublicKey.from_npub(input_str).hex()
    return input_str

def verify_API():
    relay_manager = RelayManager()
    relay_manager.add_relay("wss://nos.lol")
    relay_manager.add_relay("wss://nostr.bitcoiner.social")
    relay_manager.add_relay("wss://relay.damus.io")
    time.sleep(1.25) # allow the connections to open
    identity_pk = PrivateKey.from_nsec(os.getenv('NOSTR_PRIVATE_KEY'))
    verification_post = Event("Running Nostr Serverless API")
    identity_pk.sign_event(verification_post)
    relay_manager.publish_event(verification_post)
    time.sleep(1) # allow the messages to send
    relay_manager.close_all_relay_connections()

def send_text_note(text, private_key, relays=["wss://nos.lol", "wss://nostr.bitcoiner.social", "wss://relay.damus.io"]):
    if isinstance(relays, str):
        relays = [relays]
    relay_manager = RelayManager()
    for relay in relays:
        relay_manager.add_relay(relay)
    time.sleep(1.25) # allow the connections to open
    identity_pk = PrivateKey.from_nsec(private_key)
    verification_post = Event(text)
    identity_pk.sign_event(verification_post)
    relay_manager.publish_event(verification_post)
    time.sleep(.25) # allow the messages to send
    relay_manager.close_all_relay_connections()

def fetch_text_notes(authors, relays=["wss://nos.lol", "wss://nostr.bitcoiner.social", "wss://relay.damus.io"]):
    if isinstance(authors, str):
        authors = [authors]
    if isinstance(relays, str):
        relays = [relays]
    authors = [convert_to_hex(author) for author in authors]
    try:
        filters = Filters([Filter( authors=authors, kinds=[EventKind.TEXT_NOTE])])
        subscription_id = uuid.uuid1().hex
        request = [ClientMessageType.REQUEST, subscription_id]
        request.extend(filters.to_json_array())
        
        relay_manager = RelayManager()

        for relay in relays:
            relay_manager.add_relay(relay)

        time.sleep(1.25)
        
        relay_manager.add_subscription_on_all_relays(id= subscription_id, filters = filters)
        message = json.dumps(request)
        relay_manager.publish_message(message)
        time.sleep(2)  # allow the messages to send
        result = {}
        while relay_manager.message_pool.has_events():
            event_msg = relay_manager.message_pool.get_event()
            message_data = {}
            message_data["time_created"] =  event_msg.event.created_at
            message_data["content"] = event_msg.event.content
            message_data["author"] = event_msg.event.public_key
            message_data["tags"] = event_msg.event.tags
            message_data["signature"] = event_msg.event.signature
            result[event_msg.event.note_id] = message_data

        relay_manager.close_all_relay_connections()

        return result
    except Exception as e:
        logger.error(f'Error in fetch_text_notes function: {str(e)}')
        raise


