import io
import pandas as pd
import requests
import pyarrow as pa
import pyarrow.parquet as pq
import os

urls = [
        'https://d37ci6vzurychx.cloudfront.net/trip-data/fhv_tripdata_2019-01.parquet',
        'https://d37ci6vzurychx.cloudfront.net/trip-data/fhv_tripdata_2019-02.parquet',
        'https://d37ci6vzurychx.cloudfront.net/trip-data/fhv_tripdata_2019-03.parquet',
        'https://d37ci6vzurychx.cloudfront.net/trip-data/fhv_tripdata_2019-04.parquet',
        'https://d37ci6vzurychx.cloudfront.net/trip-data/fhv_tripdata_2019-05.parquet',
        'https://d37ci6vzurychx.cloudfront.net/trip-data/fhv_tripdata_2019-06.parquet',
        'https://d37ci6vzurychx.cloudfront.net/trip-data/fhv_tripdata_2019-07.parquet',
        'https://d37ci6vzurychx.cloudfront.net/trip-data/fhv_tripdata_2019-08.parquet',
        'https://d37ci6vzurychx.cloudfront.net/trip-data/fhv_tripdata_2019-09.parquet',
        'https://d37ci6vzurychx.cloudfront.net/trip-data/fhv_tripdata_2019-10.parquet',
        'https://d37ci6vzurychx.cloudfront.net/trip-data/fhv_tripdata_2019-11.parquet',
        'https://d37ci6vzurychx.cloudfront.net/trip-data/fhv_tripdata_2019-12.parquet'
]

data_all = pd.DataFrame()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/labber/dtc-de/mage-zoomcamp/data-engineering-409902-0ed8148f1650.json'
bucket_name = 'zoomcamp-mage-bucket'
object_key = 'nyc_fhv_2019.parquet'
root_path = f'{bucket_name}/{object_key}'

def load_data_from_api(*args, **kwargs):

    # declear data type
    taxi_dtypes = {
        'dispatching_base_num': 'object',
        'PUlocationID': pd.Int64Dtype(),
        'DOlocationID': pd.Int64Dtype(),
        'SR_Flag': pd.Int64Dtype(),
        'Affiliated_base_number': 'object',
        'pickup_datetime': pd.DatetimeTZDtype(tz='US/Eastern'),
        'dropOff_datetime': pd.DatetimeTZDtype(tz='US/Eastern')
    }

    # # timestamp data
    parse_dates = ['pickup_datetime','dropOff_datetime']

    data_list  = []

    for url in urls:

        data = pd.read_parquet(url, columns=list(taxi_dtypes.keys()), engine='pyarrow')
        for date_col in parse_dates:
            data[date_col] = pd.to_datetime(data[date_col], unit='us')
        data_list.append(data)

    data_all = pd.concat(data_list)
    return data_all


def export_data(data, *args, **kwargs):

    table = pa.Table.from_pandas(data, preserve_index=False)

    gcs = pa.fs.GcsFileSystem()

    pq.write_to_dataset(
        table,
        root_path=root_path,
        coerce_timestamps='us',
        filesystem=gcs
    )

fhv_data = load_data_from_api()
export_data(fhv_data)
