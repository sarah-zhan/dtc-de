import pandas as pd
from time import time
from sqlalchemy import create_engine
import argparse
import os

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    database = params.database
    table = params.table
    url = params.url

    csv_name = "output.csv"

    # download data
    os.system(f"wget -O {csv_name} {url}")
    # create engine
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
    # create iterator
    df_iter = pd.read_csv(csv_name, compression='gzip', chunksize=100000, iterator=True)

    df = next(df_iter)
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    # insert the header
    df.head(n=0).to_sql(name=table, con=engine, if_exists='replace')

    df.to_sql(table, engine, if_exists='append')

    # connect to the database
    engine.connect()


    while True:
        try:
            t_start = time()

            df = next(df_iter)
            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

            df.to_sql(table, engine, if_exists='append')

            t_end = time()
            print(f"inserted 100k rows, {t_end - t_start:.2f} seconds elapsed")

        except StopIteration:
            print("finished")
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres.')
    # add arguments
    parser.add_argument('--user', help='an integer for the accumulator')
    parser.add_argument('--password', help='an integer for the accumulator')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--database', help='database name')
    parser.add_argument('--table', help='table name')
    parser.add_argument('--url', help='url for csv file')

    args = parser.parse_args()

    main(args)