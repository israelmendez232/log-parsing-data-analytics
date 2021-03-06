import os
from sqlalchemy import create_engine

def get_engine(type_user: str):
    """
    # GET ENGINE

    Connects into the data warehouse.

    Parameters
    ----------
    type_user : string
        The type of the users that it's been used for to connect the database.

    Returns
    -------
    engine : connection
        Return the connection for the DW.
    """
    if type_user == 'root':
        username = os.environ['POSTGRES_USER']
        password = os.environ['POSTGRES_PASSWORD']
    else:
        username = os.environ['name_personal_user']
        password = os.environ['password_personal_user']
        
    database = os.environ['POSTGRES_DB']
    host = os.environ['DW_HOST']

    connection = f'postgresql://{username}:{password}@{host}:5432/{database}'
    engine = create_engine(connection)
    return engine

def structure_data_warehouse():
    """
    # STRUCTURE OF THE DATA WAREHOUSE

    Creates and manages the pattern for the data warehouse. Such as roles, schemas, and users.
    
    """
    engine = get_engine('root')
    password = os.environ['password_personal_user']
    username = os.environ['name_personal_user']
    
    queries = [
        # Create main roles
        "CREATE ROLE admin_user;"
        ,  "CREATE ROLE advanced_user;"
        ,  "CREATE ROLE essencial_user;"
        
        # Create the schemas to store the data
        ,  "CREATE SCHEMA IF NOT EXISTS raw;"
        ,  "CREATE SCHEMA IF NOT EXISTS trusted;"
        ,  "CREATE SCHEMA IF NOT EXISTS analytics;"
        
        # Create my user to connect and deliver the data
        ,  f"CREATE USER {username} WITH PASSWORD '{password}';"
        ,  f"GRANT admin_user TO {username};"
        
        # Grant main access to schemas and tables        
        ,  "GRANT ALL ON SCHEMA raw TO admin_user;"
        ,  "GRANT ALL ON SCHEMA trusted TO admin_user;"
        ,  "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA trusted TO advanced_user;" 
        ,  "GRANT ALL ON SCHEMA analytics TO admin_user;"
        ,  "GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA analytics TO advanced_user;" 
        ,  "GRANT SELECT ON ALL TABLES IN SCHEMA analytics TO essencial_user;"
    ]

    for query in queries:
        engine.execute(query)
        
    engine.dispose()   
    print("===> All configurations were done!")
