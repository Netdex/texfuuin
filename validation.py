
from config import config


def str_constrain_len(s, limit):
    return s and type(s) is str and len(s) <= limit


def validate_post(post):
    if not str_constrain_len(post.get('user'), config['uname_limit']):
        return 'uname-limit'
    if not str_constrain_len(post.get('message'), config['message_limit']):
        return 'message-limit'
    if not post.get('parent'):
        if not str_constrain_len(post.get('title'), config['title_limit']):
            return 'title-limit'
    return None
