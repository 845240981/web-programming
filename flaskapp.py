from flask import Flask

from flask import Response


flask_app =Flask('flaskapp')


@flask_app.route('/hi')
def hello_world():
    return Response(
        'Hello world from Flask!\n'

    )
app =flask_app.wsgi_app