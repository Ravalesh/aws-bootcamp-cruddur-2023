from datetime import datetime, timedelta, timezone

from lib.ddb import Ddb
from lib.db import db

class MessageGroups:
  def run(cognito_user_id):
    model = {
      'errors': None,
      'data': None
    }

    sql = db.load_template('db', 'sql', 'users', 'uuid_from_cognito_user_id')
    my_user_uuid = db.fetch_object_json(sql, cognito_user_id=cognito_user_id)

    print(f"UUID: {my_user_uuid}")

    ddb = Ddb.client()
    data = Ddb.list_message_groups(ddb, my_user_uuid['uuid'])
    print("list_message_groups: ", data)

    #MomentoCounter.reset(f"msgs/{user_handle}")
    model['data'] = data
    return model