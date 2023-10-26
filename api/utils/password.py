import hashlib
from data.config import HASH_SALT


def hash_password(password: str, salt: str = HASH_SALT) -> str:
    # Create a new sha256 hash object
    sha256 = hashlib.sha256()

    # Hash the password along with the salt
    sha256.update(salt.encode('utf-8'))
    sha256.update(password.encode('utf-8'))

    # Return the salt and the hexadecimal representation of the hash
    print(sha256.hexdigest())
    return sha256.hexdigest()


