import hashlib
from config import config


def triphash(trip):
    return hashlib.sha1((trip + config['trip_salt']).encode('utf-8')).hexdigest()[-7:]


def tripcode(user):
    sp = user.partition('#')
    if not sp[2]:
        return sp[0], ''
    return sp[0], triphash(sp[2])