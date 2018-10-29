# -*- coding: utf-8 -*-
from base64 import b64decode
from bottle import run, Bottle
from wsgiproxy import HostProxy


def unauthorized():
    return (
        '401 Unauthorized',
        None,
        [
            (
                'WWW-Authenticate',
                'Basic realm="Credentials required", charset="UTF-8"',
            ),
        ],
        [],
    )


class MyHostProxy(HostProxy):
    def process_request(self, uri, method, headers, environ):
        print(headers)

        # search to authenticate user
        if 'Authorization' not in headers:
            print('no header Authorization !')
            return unauthorized()

        auth = b64decode(headers['Authorization'].split('Basic ')[1])
        login = auth.decode().split(':')[0]

        if not login.startswith('bastien'):
            print('only bastien allowed !')
            return unauthorized()

        return self.http(uri, method, environ['wsgi.input'], headers)


app = Bottle()
proxy = MyHostProxy(
    "http://127.0.0.1:4321",
    allowed_methods=[
        'GET',
        'HEAD',
        'POST',
        'PUT',
        'DELETE',
        'OPTIONS',

        'PROPFIND',
        'PROPPATCH',
        'REPORT',
        'MKCOL',
        'MKCALENDAR',
        'ACL',
    ]
)
app.mount("/radicale", proxy)

run(app=app, host='127.0.0.1', port=8080, debug=True)
