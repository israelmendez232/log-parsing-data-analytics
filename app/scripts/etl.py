import os
import pandas as pd
from data_warehouse import get_engine
from datetime import datetime

def raw_zone(engine_db, table: str):
    """
    # RAW ZONE

    Transform the JSON data into a tabular format for the `trusted` schema/dataset.

    Parameters
    ----------
    engine_db : connection
        The connection to send data into the data warehouse
    table : str
        The table name will be used to save into the storage and data warehouse.
    """
    log_file = "./logs/nginx.log"

    df = pd.read_csv(log_file,
              sep=r'\s(?=(?:[^"]*"[^"]*")*[^"]*$)(?![^\[]*\])',
              engine='python',
              usecols=[0, 3, 4, 5, 6, 7, 8],
              names=['ip', 'time', 'request', 'status_code', 'size', 'referer', 'user_agent'],
              na_values='-',
              header=None
            )

    # Partitions
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    refdate = now.strftime("%Y%m%d")
    reftime = now.strftime("%H%M%S")

    df['year'] = year
    df['month'] = month
    df['day'] = day
    df['reftime'] = reftime
    df['refdate'] = refdate
    
    # Insert the final data
    schema = 'raw'
    df.to_sql(table, engine_db, schema, index = False, if_exists = 'append')
    print(f"===> Success to save {schema}.{table}.")

def trusted_zone(engine_db, table: str):
    """
    # TRUSTED ZONE

    Transform the JSON data into a tabular format for the `TRUSTED` schema/dataset.

    Parameters
    ----------
    engine_db : connection
        The connection to send data into the data warehouse
    table : str
        The table name will be used to save into the storage and data warehouse.
    """
    schema = 'trusted'
    drop_old_table = f"DROP TABLE IF EXISTS {schema}.{table};"
    new_table = f"""
        CREATE TABLE {schema}.{table} AS 
        SELECT * 
        FROM raw.{table} 
        WHERE refdate = (SELECT MAX(refdate) FROM raw.{table}) 
            AND reftime = (SELECT MAX(reftime) FROM raw.{table})
    """

    engine_db.execute(drop_old_table)
    engine_db.execute(new_table)
    print(f"===> Success to save {schema}.{table}.")

def main():
    engine = get_engine('admin')
    raw_zone(engine, 'logs')
    trusted_zone(engine, 'logs')
    engine.dispose()

    print("===> Done with all the ETL!")
