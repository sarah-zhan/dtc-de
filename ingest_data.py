import pandas as pd
from time import time
from sqlalchemy import create_engine

# read data
df = pd.read_csv('yellow_tripdata_2021-01.csv.gz', compression='gzip')

# create engine
engine = create_engine('postgresql://labber:labber@localhost:5432/ny_taxi')

engine.connect()

# insert the header
df.head(n=0).to_sql('yellow_taxi_data', engine, if_exists='replace')


df_iter = pd.read_csv('yellow_tripdata_2021-01.csv.gz', compression='gzip', chunksize=100000, iterator=True)
while True:
    try:
        t_start = time()

        df = next(df_iter)
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

        df.to_sql('yellow_taxi_data', engine, if_exists='append')

        t_end = time()
        print(f"inserted 100k rows, {t_end - t_start:.2f} seconds elapsed")

    except StopIteration:
        print("finished")
        break

