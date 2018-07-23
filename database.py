from tinydb import TinyDB, Query
import uuid

from config import config

db = TinyDB(config['db_path'])


def all_threads():
    # TODO pagination
    post = Query()
    threads = db.search(~post.parent.exists())
    rthreads = []
    for thread in threads:
        rthread = thread.copy()
        rthread['replies'] = get_thread_replies(uuid.UUID(thread['id']))
        rthreads.append(rthread)
    return rthreads


def get_thread_replies(parent_id):
    """
    Get all replies to a thread
    If the thread does not exist, return an empty list
    :param parent_id: Thread ID
    :return: replies to thread
    """
    assert type(parent_id) is uuid.UUID, """parent_id is not correct type"""
    reply_query = Query()
    results = db.search(reply_query.parent == str(parent_id))
    return results


def get_post_by_id(post_id):
    """
    Gets post object w/ replies by ID
    If the post does not exist, return none
    :param post_id: Post ID to get post object
    :return: Post object by ID
    """
    assert type(post_id) is uuid.UUID, """post_id is not correct type"""
    post_query = Query()
    results = db.get(post_query.id == str(post_id))
    if results:
        thread = results.copy()
        if not results.get('parent'):
            thread['replies'] = get_thread_replies(post_id)
        return thread
    return None


def has_post(post_id):
    """
    Check if post ID exists in db
    :param post_id: Post ID to check
    :return: Whether the post ID exists in db
    """
    assert type(post_id) is uuid.UUID, """post_id is not correct type"""
    post = Query()
    return db.contains(post.id == str(post_id))


def add_post(post):
    """
    Add validated post into db
    :param post: Validated thread/reply object
    :return: Whether the operation succeeded
    """
    if post.get('parent') and not has_post(uuid.UUID(post['parent'])):
        return False
    db.insert(post)
    return True


def delete_post(post_id):
    """
    Delete post and all children by post ID.
    Does not check if the post exists before deleting.
    :param post_id: ID of the post to delete
    :return: None
    """
    assert type(post_id) is uuid.UUID, """post_id is not correct type"""
    post = Query()
    db.remove((post.id == str(post_id)) | (post.parent == str(post_id)))
