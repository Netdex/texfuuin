from gevent.pywsgi import WSGIServer
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import uuid

from config import config
import validation
from tripcode import tripcode, triphash
import filter
import database as db
import post

app = Flask(__name__)
app.register_blueprint(filter.blueprint)


@app.route('/edit', methods=['POST'])
def rt_edit():
    u_action = request.form.get('action')
    u_tripcode = request.form.get('tripcode')
    u_post_id = request.form.get('postid')

    # form validation
    post_id = validation.validate_uuid(u_post_id)
    if not post_id:
        return redirect(url_for('rt_post', error='post-id'))
    post_obj = db.get_post_by_id(post_id)
    if not post_obj:
        return redirect(url_for('rt_post', error='post-id'))

    # find uppermost thread of current post
    parent_thread = uuid.UUID(post_obj['parent']) if post_obj.get('parent') else post_id
    uhash = triphash(u_tripcode)
    if post_obj['tripcode'] != uhash and config['admin_trip'] != uhash:
        return redirect(url_for('rt_post',
                                post_id=parent_thread,
                                error='no-auth'))

    captcha_resp = request.form.get('g-recaptcha-response')
    if not validation.validate_captcha(captcha_resp):
        return redirect(url_for('rt_post', error='captcha', post_id=parent_thread))

    # do action based on form param
    if u_action == 'delete':
        if not db.has_post(post_id):
            return redirect(url_for('rt_post', error='post-id'))
        db.delete_post(post_id)
        return redirect(url_for('rt_index'))

    return redirect(url_for('rt_post', error='unspecified'))


@app.route('/new', methods=['POST'])
@app.route('/new/<uuid:post_id>', methods=['POST'])
def rt_new(post_id=None):
    captcha_resp = request.form.get('g-recaptcha-response')
    if not validation.validate_captcha(captcha_resp):
        return redirect(url_for('rt_post', error='captcha', post_id=post_id))

    post_obj = post.new_post(
        user=request.form.get('user'),
        message=request.form.get('message'),
        title=request.form.get('title'),
        parent=post_id
    )

    # validation and error process
    validation_error = validation.validate_post(post_obj)
    if validation_error:
        return redirect(url_for('rt_post', error=validation_error, post_id=post_id))

    # tripcode process
    post_obj['user'], post_obj['tripcode'] = tripcode(post_obj['user'])

    # post does not have parent
    if post_id is None:
        db.add_post(post_obj)
    # post has parent
    else:
        if db.add_post(post_obj):
            # redirect back to original parent post so user can see added post
            return redirect(url_for('rt_post', post_id=post_id))

        # redirect back to post with error since parent invalid
        return redirect(url_for('rt_post', error='post-id'))

    # redirect to newly created thread
    return redirect(url_for('rt_post', post_id=post_obj['id']))


@app.route('/post')
@app.route('/post/<uuid:post_id>')
def rt_post(post_id=None):
    parent_thread = {}
    # check if post is new thread
    if post_id is not None:
        # find parent thread to post reply
        results = db.get_post_by_id(post_id)
        # check if parent thread exists
        if not results:
            return redirect(url_for('rt_post', error='post-id'))
        parent_thread.update(results)

    # display post form with given parent if exists
    return render_template('post.html',
                           thread=parent_thread or None,
                           config=config,
                           error=request.args.get('error'))


@app.route('/')
def rt_index():
    return render_template('index.html', threads=db.all_threads(), config=config)


if __name__ == '__main__':
    if config['devel']:
        app.run()
    else:
        http_server = WSGIServer(('', config['port']), app)
        http_server.serve_forever()
