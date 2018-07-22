from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from tinydb import TinyDB, Query
import uuid

from config import config
import validation
from tripcode import tripcode

app = Flask(__name__)
db = TinyDB(config['db_path'])


@app.route('/new', methods=['POST'])
@app.route('/new/<uuid:post_id>', methods=['POST'])
def rt_new(post_id=None):
    post_obj = {
        'user': request.form.get('user'),
        'message': request.form.get('message'),

        'id': str(uuid.uuid4()),
        'datetime': str(datetime.now())
    }

    # post does not have parent
    if post_id is None:
        post_obj.update({
            'title': request.form.get('title'),
        })
    # post has parent
    else:
        post_obj.update({
            'parent': str(post_id)
        })

    validation_error = validation.validate_post(post_obj)
    if validation_error:
        return redirect(url_for('rt_post', error=validation_error, post_id=post_id))

    post_obj['user'], post_obj['tripcode'] = tripcode(post_obj['user'])

    # post does not have parent
    if post_id is None:
        db.insert(post_obj)
    # post has parent
    else:
        post_query = Query()
        results = db.search(post_query.id == str(post_id))
        if results:
            post_reply = results[0]
            if post_reply.get('replies') is None:
                post_reply['replies'] = []
            post_reply['replies'].append(post_obj)
            reply_query = Query()
            db.update(post_reply, reply_query.id == str(post_id))
            return redirect(url_for('rt_post', post_id=post_id))
        return redirect(url_for('rt_post', error='post-id'))
    return redirect(url_for('rt_post', post_id=post_obj['id'] if post_id is None else post_id))


@app.route('/post')
@app.route('/post/<uuid:post_id>')
def rt_post(post_id=None):
    results = []
    if post_id is not None:
        post_query = Query()
        results += db.search(post_query.id == str(post_id))
        if not results:
            return redirect(url_for('rt_post', error='post-id'))
    return render_template('post.html',
                           thread=results[0] if results else None,
                           config=config,
                           error=request.args.get('error'))


@app.route('/')
def rt_index():
    return render_template('index.html', threads=db.all(), config=config)


if __name__ == '__main__':
    app.run()
