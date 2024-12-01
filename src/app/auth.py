from functools import wraps

import werkzeug.exceptions

from flask import request
from joserfc import jwt
from joserfc.errors import JoseError
from werkzeug.datastructures import WWWAuthenticate

def authorize(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        def get_token(auth):
            try:
                return jwt.decode(auth.token, '')
            except JoseError as e:
                raise werkzeug.exceptions.Unauthorized(www_authenticate=WWWAuthenticate("bearer", {"realm": "mentorHub", "error": e.error, "error_description": e.description}))
            # Since `request.authorization` either returns an Authorization object or None, an AttributeError will be raised when the header is missing or lacks a token
            except AttributeError:
                # Exclude error information as per RFC 6750 section 3.1
                raise werkzeug.exceptions.Unauthorized(www_authenticate=WWWAuthenticate("bearer", {"realm": "mentorHub"}))

        token = get_token(request.authorization)

        if request.path == '/api/topic' and request.method == 'POST':
            try:
                if "Mentor" in token.claims['roles']:
                    authorized = True
                else:
                    authorized = False
            except KeyError:
                authorized = False
        else:
            authorized = True

        if authorized:
            return f(*args, **kwargs)
        else:
            raise werkzeug.exceptions.Forbidden()


    return decorated_function
