import uuid
from datetime import datetime


def new_post(user, message, title=None, parent=None):
    post_obj = {
        'user': user,
        'message': message,
        'id': str(uuid.uuid4()),
        'datetime': datetime.now().timestamp()
    }

    # post does not have parent
    if parent is None:
        post_obj.update({
            'title': title,
        })
    # post has parent
    else:
        post_obj.update({
            'parent': str(parent)
        })

    return post_obj
