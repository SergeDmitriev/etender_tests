import pyodbc
from db_layer import config


def send_query(input_sql_query):
    with pyodbc.connect(
            "DRIVER={driver}; server={server};database={database};uid={uid};pwd={pwd}"
                    .format(driver='SQL Server',
                            server=config.SERVER,
                            database=config.DATABASE,
                            uid=config.USER_ID,
                            pwd=config.PASSWORD)) as con:
        cur = con.cursor()
        cur.execute(input_sql_query)
        r = []
        for row in cur:
            r.append(row)
    return r


if __name__ == '__main__':
    pass

