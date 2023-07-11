import time
import os
from nostr.relay_manager import RelayManager
from nostr.key import PrivateKey
from nostr.event import EncryptedDirectMessage,Event
from nostr.delegation import Delegation

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