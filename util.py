import hashlib




def plaintext_to_hash(plaintext):
    hasher = hashlib.sha256()
    hasher.update(plaintext.encode("utf-8"))
    return hasher.hexdigest()

# Test
string = "tringeling"
hash1 = plaintext_to_hash(string)
hash2 = plaintext_to_hash(string)

if hash1==hash2:
    print("Yesy")
else:
    print("{},{}".format(hash1,hash2))


