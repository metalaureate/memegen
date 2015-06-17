from collections import OrderedDict

from flask import Blueprint, current_app as app, url_for, redirect

from ..domain import Image, Text


blueprint = Blueprint('links', __name__, url_prefix="/")


@blueprint.route("<key>/<path:path>")
def get(**kwargs):
    """Get links for generated images."""
    data = OrderedDict()
    data['visible'] = OrderedDict()
    data['hidden'] = OrderedDict()
    text = Text(kwargs['path'])
    if kwargs['path'] != text.path:
        kwargs['path'] = text.path
        return redirect(url_for(".get", **kwargs))
    for kind in Image.KINDS:
        url = url_for('image.get', kind=kind.lower(), _external=True, **kwargs)
        data['visible'][kind] = url
        code = app.link_service.encode(**kwargs)
        url = url_for('image.get_encoded', kind=kind.lower(), _external=True,
                      code=code)
        data['hidden'][kind] = url
    return data


@blueprint.route("<code>")
def get_encoded(code):
    key, path = app.link_service.decode(code)
    url = url_for('.get', key=key, path=path)
    return redirect(url)
