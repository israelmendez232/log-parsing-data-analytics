from data_warehouse import structure_data_warehouse
from simulate_logs import insert_log
from analytics import get_data_dw
import etl
import time

# 1. Configure the right settings for the DW
try:
    structure_data_warehouse() 
except:
    print("===> Configurations already set on DW.")
    pass

# 2. Loop to handle all scripts
while True:
    # 2.1 Insert new logs
    insert_log() 
    time.sleep(5) 

    # 2.2 Make the ETL details
    etl.main() 
    time.sleep(2) 

    # 2.3 Get the results for few "questions"
    query = f'SELECT COUNT(*) AS requests, status_code FROM trusted.logs GROUP BY status_code ORDER BY requests DESC'
    result = get_data_dw(query)
    print("===> Results based on requests and status_code:")
    print(result)
    time.sleep(2) 
