import jinja2
import flask
from datetime import datetime

blueprint = flask.Blueprint('filters', __name__)


@jinja2.contextfilter
@blueprint.app_template_filter()
def ctime(context, ts):
    return datetime.fromtimestamp(ts).ctime()