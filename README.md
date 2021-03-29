# Log Parsing - Data Analytics
A solution to read a log file from an [Nginx](https://www.nginx.com/) application and parse it into a SQL database for analytics.

## Summary
1. [Steps to run](#1-steps-to-run) <br>
2. [Architecture](#2-architecture) <br>
  2.1 [Data Warehouse](#21-data-warehouse) <br>
  2.2 [Services Management](#22-services-management) <br>
  2.3 [Data](#23-data) <br>
  2.4 [ETL](#24-etl)

## 1. Steps to Run
1. Git clone this repository and move into it:
``` bash
git clone https://github.com/israelmendez232/log-parsing-data-analytics.git
cd ./log-parsing-data-analytics
```

2. Modify and copy the `.env.sample` with the credentials you may prefer:
``` bash
cd ./app
cp .env.sample .env
```

3. Enter on the `app` folder where the scripts are running. And run the containers:
``` bash
docker-compose up
```

**IMPORTANT:** You will have to wait a few minutes to start all the configurations, installation, and the code itself to run. Because the ETL will wait until the data warehouse will be ready to be used.

The application will print every step, such as the ETL and the results for analytics based on the request on the status code. 

## 2. Architecture
The main elements of the application and pipeline: <br>
![Main Architecture](images/main_architecture.png "Application and Pipeline")

The steps:
1. **Data:** an application generates a file `nginx.log` with all what it's happening inside and the requests;
2. **Services Management:** Using [docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/) to manage all services;
3. **ETL:** Uses [Python](https://www.python.org/) to transform and load the data into the Data Warehouse;
4. **Data Warehouse:** Using [PostgreSQL](https://www.postgresql.org/) to store the data to read.

### 2.1 Data Warehouse
The storage of the data is using [PostgreSQL](https://www.postgresql.org/). The main pattern here is to divide the DW into schemas with specific purposes:
1. **Raw:** Receive the raw log data and add it inside of the DW, in a structured format. Adding with partitions;
2. **Trusted:** Retrieve the data in raw, collects the last partition, and provide consistent numbers.

Here is a table to be more clear:
| **Zones** | **Partition** | **Source** |
|-----------|---------------|------------|
| Raw       | Yes           | Logs       |
| Trusted   | No            | Raw        |

The objective is to break into roles the type of access of the data warehouse:
| **Type of User** | **Example**                  | **Raw** | **Trusted** |
|------------------|------------------------------|---------|-------------|
| Essential        | Marketing, Product           | No      | Yes         |
| Advanced         | Data Analyst, Data Scientist | No      | Yes         |
| Admin            | Data Engineer, DevOps        | Yes     | Yes         |


### 2.2 Services Management
The whole application is running on docker and docker-compose. It's based on these two containers:
- **PostgreSQL:** from their official image on [dockerhub](https://hub.docker.com/_/postgres);
- **Python:** a custom image that I've built on `dockerfile`. 

Also, the `./app/scripts/orchestration.py` helps to manage [PostgreSQL](https://www.postgresql.org/) access, users, and the simulation of the logs itself, along with the ELT.

### 2.3 Data
The data is a log that's been written by the time. A script simulates this input to writing new lines, you can check it on `./app/scripts/simulate_logs.py`.

### 2.4 ETL
The code that "extract" and transform the data into a tabular format to be consumed on SQL. The script is located on `./app/scripts/etl.py`. Is separated on:
- `raw_zone`: Script that reads the log, transform using regex into a dataframe. Adds partitions and move the data into the data warehouse;
- `trusted_zone`: Script that selects the last partition and moves to a `trusted` schema.
