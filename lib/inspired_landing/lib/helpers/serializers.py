""" serializers files handles any data format transpose functions """
import json
import datetime

class JSONEncoder(json.JSONEncoder):
    """
    Wrapper class to try calling an object's tojson() method. This allows
    us to JSONify objects coming from the ORM. Also handles dates and datetimes.
    """

    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.isoformat()

        try:
            return obj.tojson()
        except AttributeError:
            return json.JSONEncoder.default(self, obj)

