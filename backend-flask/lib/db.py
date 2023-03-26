from psycopg_pool import ConnectionPool
import os

class Db:
  def __init__(self):
    self.init_pool()

  def init_pool(self):
    connection_url = os.getenv("CONNECTION_URL")
    self.pool = ConnectionPool(connection_url)

  def query_wrap_object(self, template):
    sql = f"""
    (SELECT COALESCE(row_to_json(object_row),'{{}}'::json) FROM (
    {template}
    ) object_row);
    """
    return sql

  def query_wrap_array(self, template):
    sql = f"""
    (SELECT COALESCE(array_to_json(array_agg(row_to_json(array_row))),'[]'::json) FROM (
    {template}
    ) array_row);
    """
    return sql

  # When we want to commit data to database
  def sql_commit(self, sql):
    try:
      with self.pool.connection() as conn:
        with conn.execute() as cur:
          cur.execute(sql)
          conn.commit()
    except Exception as err:
      print(err)
      #conn.rollback()

  # When we want to fetch array of objects
  def fetch_array_json(self, template):
    try:
      wrapped_sql = self.query_wrap_array(template)
      with self.pool.connection() as conn:
          with conn.cursor() as cur:
            cur.execute(wrapped_sql)
            # this will return a tuple
            # the first field being the data
            json = cur.fetchone()
            return json[0]
    except Exception as err:
      print(err)
      return ''

  # When we want to return single object
  def fetch_object_json(self, template):
    try:
      wrapped_sql = self.query_wrap_object(template)
      with self.pool.connection() as conn:
          with conn.cursor() as cur:
            cur.execute(wrapped_sql)
            # this will return a tuple
            # the first field being the data
            json = cur.fetchone()
            return json[0]
    except Exception as err:
      print(err)
      return ''


db = Db()
