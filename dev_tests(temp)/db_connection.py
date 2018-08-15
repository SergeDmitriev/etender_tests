# import sqlalchemy as sa
# from sqlalchemy import create_engine
# from sqlalchemy.engine.url import make_url
# from sqlalchemy.sql import text
#
# from db_layer.config import USER_ID, PASSWORD, SERVER, DATABASE
#
# credentials = {
#     'username': USER_ID,
#     'password': PASSWORD,
#     'host': SERVER,
#     'database': DATABASE}
#
# connect_url = sa.engine.url.URL(
#     'mssql+pyodbc',
#     username=credentials['username'],
#     password=credentials['password'],
#     host=credentials['host'],
#     database=credentials['database'],
#     query=dict(driver='SQL Server Native Client 11.0'))
#
#
# def set_connection():
#     engine = create_engine(connect_url)
#     connection = engine.connect()
#     return connection
#
#
# def simple_select(sql_statement):
#     conn = set_connection()
#     s = text(sql_statement)
#     return conn.execute(s).fetchall()
pass

if __name__ == '__main__':
    pass


