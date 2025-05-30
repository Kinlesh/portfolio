# chatbot/utils.py
import hashlib

def hash_value(value):
    """Verilen değeri SHA-256 ile hashler."""
    return hashlib.sha256(value.encode()).hexdigest()
