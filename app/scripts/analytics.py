import pandas as pd
from data_warehouse import get_engine

def get_data_dw(query: str):
    engine = get_engine('admin')
    df = pd.read_sql_query(query, con = engine)
    result = df.to_string(index=False)
    engine.dispose()
    return result
