import pandas as pd
from random import randrange

def insert_log():
    log_file = "./logs/nginx.log"
    df = pd.read_csv(log_file, delimiter = "\t", sep=" ", header=None)
    lines = len(df.index) + 1 # To make sure that every line will be selected

    # Selecting the right number of lines to input
    rows_init = randrange(lines)
    rows_end = rows_init + randrange(11)
    new_df = df[rows_init:rows_end]
    new_list = new_df.values.tolist()
    
    # Writing the logs
    with open(log_file, "a") as file_object:
        for element in new_list:
            log = element[0]
            file_object.write(f"{log}\n")
    print("===> Writting the log.")
