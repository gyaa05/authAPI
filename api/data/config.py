from os import getenv


JWT_SECRET = getenv("jwt_secret")
JWT_ALGORITHM = getenv("jwt_algorithm")

HASH_SALT = getenv("hash_salt")
