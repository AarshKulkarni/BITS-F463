import hashlib


def simple_hash(value: str):
    hash_object = hashlib.sha256(value.encode())
    return hash_object.hexdigest()[:16]
