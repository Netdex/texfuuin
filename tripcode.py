import hashlib
from config import config


def tripcode(user):
    sp = user.partition('#')

    if not sp[2]:
        return sp[0], ''

    return sp[0], hashlib.sha1((sp[2] + config['trip_salt']).encode('utf-8')).hexdigest()[-7:]