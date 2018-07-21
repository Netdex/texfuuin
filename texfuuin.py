from flask import Flask
from flask import render_template
from datetime import datetime

app = Flask(__name__)


@app.route('/post')
@app.route('/post/<int:id>')
def rt_post(id=None):
    return render_template('post.html', thread={
        "id": 2013923,
        "parent": 219320,
        "user": "anonymous",
        "datetime": datetime.now(),
        "title": "why you so tho",
        "message": "idk why is it like the way it is",
        "replies": [
            {
                "id": 2013923,
                "parent": 219320,
                "user": "anonymous",
                "datetime": datetime.now(),
                "message": "yeah that's why",
            }
        ]
    })


@app.route('/')
def rt_index():
    return render_template('index.html', threads=[
        {
            "id": 2013923,
            "parent": 219320,
            "user": "anonymous",
            "datetime": datetime.now(),
            "title": "why you so tho",
            "message": "idk why is it like the way it is",
            "replies": [
                {
                    "id": 2013923,
                    "parent": 219320,
                    "user": "anonymous",
                    "datetime": datetime.now(),
                    "message": "yeah that's why",
                }
            ]
        },
        {
            "id": 2013923,
            "parent": 219320,
            "user": "anonymous",
            "datetime": datetime.now(),
            "title": "why you so tho",
            "message": "idk why is it like the way it is",
            "replies": [
                {
                    "id": 2013923,
                    "parent": 219320,
                    "user": "anonymous",
                    "datetime": datetime.now(),
                    "message": "yeah that's why",
                }
            ]
        }
    ])


if __name__ == '__main__':
    app.run()
