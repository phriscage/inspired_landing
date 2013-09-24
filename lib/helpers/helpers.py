""" model helpers used for each child model """
from sqlalchemy.orm import MapperExtension
import datetime
import json

class BaseExtension(MapperExtension):
    """Base entension class for all entity """

    def before_insert(self, mapper, connection, instance):
        """ set the created_at  """
        datetime_now = datetime.datetime.now()
        instance.created_at = datetime_now
        if not instance.updated_at:
            instance.updated_at = datetime_now

    def before_update(self, mapper, connection, instance):
        """ set the updated_at  """
        instance.updated_at = datetime.datetime.now()

 
def to_json(instance, model):
    """ Returns a JSON representation of an SQLAlchemy-backed object.
    """
    json = {}
    json['fields'] = {}
    json['pk'] = getattr(model, 'id')
 
    for col in model._sa_class_manager.mapper.mapped_table.columns:
        print col
        json['fields'][col.name] = getattr(model, col.name)
 
    return json.dumps([json])

