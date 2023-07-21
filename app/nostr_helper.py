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

def send_text_note(text, private_key, relays):
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

def send_dm(text, private_key, public_key, relays):
    if isinstance(relays, str):
        relays = [relays]
    relay_manager = RelayManager()
    for relay in relays:
        relay_manager.add_relay(relay)
    time.sleep(1.25) # allow the connections to open
    identity_pk = PrivateKey.from_nsec(private_key)
    public_key = convert_to_hex(public_key)
    dm = EncryptedDirectMessage(
        recipient_pubkey=public_key,
        cleartext_content=text
        )
    identity_pk.sign_event(dm)
    relay_manager.publish_event(dm)
    time.sleep(.25) # allow the messages to send
    relay_manager.close_all_relay_connections()

def find_request_relay(request_data):
    relays = request_data.get('relays')
    if relays:
        if isinstance(relays, str):
            relays = [relays]
    else:
        relays = ["wss://relay.nostr.band/all"]
    return relays


def find_request_authors(request_data):
    authors = request_data.get('authors')
    if authors:
        if isinstance(authors, str):
            authors = [authors]
        authors = [convert_to_hex(author) for author in authors]
    return authors

def find_request_refs(request_data, name_of_ref):
    refs = request_data.get(name_of_ref)
    if refs:
        if isinstance(refs, str):
            refs = [refs]
    return refs

def generate_fetch_note_filter(request_data):
    event_filter = Filter(kinds=[EventKind.TEXT_NOTE])
    event_filter.authors = find_request_authors(request_data)
    event_filter.event_refs = find_request_refs(request_data, "event_refs")
    event_filter.pubkey_refs = find_request_refs(request_data, "pubkey_refs")
    event_filter.since = request_data.get('since')
    event_filter.until = request_data.get('until')
    limit = request_data.get('limit')
    if limit:
        event_filter.limit = limit
    else:
        event_filter.limit = 2000
    return event_filter
    
    

def fetch_text_notes(event_filter, relays):
    try:
        filters = Filters([event_filter])
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
        time.sleep(1.25)  # allow the messages to send
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


