import hashlib

hasher = hashlib.sha256()


def plaintext_to_hash(plaintext):
    hasher.update(plaintext.encode("utf-8"))

    return hasher.hexdigest()
