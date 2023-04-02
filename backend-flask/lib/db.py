from psycopg_pool import ConnectionPool
import os
from flask import current_app as app

class Db:
  def __init__(self):
    self.init_pool()

  def print_sql(self, sql):
    cyan = '\033[96m'
    no_color = '\033[0m'
    print(f'{cyan} {sql} {no_color}')

  def init_pool(self):
    connection_url = os.getenv("CONNECTION_URL")
    self.pool = ConnectionPool(connection_url)

  def load_template(self, *args):
  
    pathing = list((app.root_path,) + args)
    pathing[-1] = pathing[-1] + ".sql"

    template_path = os.path.join(*pathing)
    print(template_path)
    with open(template_path) as reader:
      template_content = reader.read()
    return template_content


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
  def sql_commit(self, sql, **kwargs):

    self.print_sql(f'SQL Statement: {sql}')
    try:
      with self.pool.connection() as conn:
        with conn.cursor() as cur:
          cur.execute(sql, kwargs)
          conn.commit()
    except Exception as err:
      print(err)
      #conn.rollback()

  # When we want to commit data to database and return the inserted id
  def sql_commit_with_returning_id(self, sql, **kwargs):
    self.print_sql(f'SQL Statement: {sql}')

    try:
      with self.pool.connection() as conn:
        with conn.cursor() as cur:
          cur.execute(sql, kwargs)
          last_id = cur.fetchone()[0]
          conn.commit()
          return last_id
    except Exception as err:
      print(err)
      #conn.rollback()

  # When we want to fetch array of objects
  def fetch_array_json(self, template, **kwargs):
    try:
      wrapped_sql = self.query_wrap_array(template)
      self.print_sql(f'SQL Statement: {wrapped_sql}')


      with self.pool.connection() as conn:
          with conn.cursor() as cur:
            cur.execute(wrapped_sql, kwargs)
            # this will return a tuple
            # the first field being the data
            json = cur.fetchone()
            if json is not None and len(json) > 0:
              return json[0]
            else:
              return "[]"
    except Exception as err:
      print(err)
      return ''

  # When we want to return single object
  def fetch_object_json(self, template, **kwargs):
    try:
      wrapped_sql = self.query_wrap_object(template)
      self.print_sql(f'SQL Statement: {wrapped_sql}')

      with self.pool.connection() as conn:
          with conn.cursor() as cur:
            cur.execute(wrapped_sql, kwargs)
            # this will return a tuple
            # the first field being the data
            json = cur.fetchone()
            if json is not None and len(json) > 0:
              return json[0]
            else:
              return "{}"
    except Exception as err:
      print(err)
      return ''


db = Db()
