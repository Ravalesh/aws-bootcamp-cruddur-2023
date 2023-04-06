from lib.db import db

class UsersShort:
  def run(handle):
    sql = db.load_template('db', 'sql', 'users', 'short')
    results = db.fetch_object_json(sql,
      handle=handle
    )
    return results