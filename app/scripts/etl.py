import os
import pandas as pd
from data_warehouse import get_engine
from datetime import datetime

def raw_zone(engine_db, table: str):
    log_file = "../logs/ngix.log"

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
    time = now.strftime("%H%M%S")

    df['year'] = year
    df['month'] = month
    df['day'] = day
    df['refdate'] = refdate
    
    # Insert the final data
    schema = 'raw'
    df.to_sql(table, engine_db, schema, index = False, if_exists = 'append')
    print("===> Success to save {schema}.{table}.")

def trusted_zone(engine, table: str):
    query = "INSERT INTO trusted.{table} SELECT * FROM raw.{table} WHERE refdate = (SELECT MAX(refdate) FROM raw.{table})"
    engine.execute(query)
    print("===> Success to save {schema}.{table}.")

def main():
    engine = get_engine('admin')
    raw_zone(engine, 'logs')
    trusted_zone(engine, 'logs')
    engine.dispose()

    print("===> Done with all ETL!")