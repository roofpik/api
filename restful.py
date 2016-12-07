from flask_restful import Resource as BaseResource
from flask.ext.mysql import MySQL
from functools import wraps


def exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception, e: # Don't use baseclass anywhere,
                            # you must rewrite the codeblock, and
                            # pust each exception for each case
            return {'error': str(e)}
    return wrapper


class Resource(BaseResource):
    method_decorators = [exception, ]

    @property
    def conn(self):
        mysql = MySQL()
        return mysql.get_db()
