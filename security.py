import hmac
import hashlib

SECRET_KEY = b"cn_project_key"

def generate_hmac(message):
    return hmac.new(SECRET_KEY, message.encode(), hashlib.sha256).hexdigest()

def verify_hmac(message, received_hmac):
    calculated = generate_hmac(message)
    return hmac.compare_digest(calculated, received_hmac)