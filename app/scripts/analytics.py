import pandas as pd
from data_warehouse import get_engine

def get_data_dw(query: str):
    """
    # GET DATA FROM DATA WAREHOUSE

    Connect into the DW and run a query.

    Parameters
    ----------
    query : string
        The SQL code to run into the database.

    Returns
    -------
    result : string
        Return the result of the query as a string.
    """
    engine = get_engine('admin')
    df = pd.read_sql_query(query, con = engine)
    result = df.to_string(index=False)
    engine.dispose()
    return result
