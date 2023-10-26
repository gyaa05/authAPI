import time
from typing import Literal

import jwt

from data.config import JWT_SECRET, JWT_ALGORITHM

def sign_jwt(id_type: Literal["admin", "organisation"],
             id_: int, jwt_type: Literal["admin", "organisation"], expire_time: int, admin: bool = False) -> str:
    payload = {
        id_type: id_,
        "type": jwt_type,
        "expires": time.time() + expire_time
    }
    if admin:
        payload["admin"] = admin
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token


def decode_jwt(token: str):
    """
    :param token: jwt token
    :return:
    :rtype: None | dict
    """
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except:
        return None
    return decoded_token if decoded_token["expires"] >= time.time() else None
