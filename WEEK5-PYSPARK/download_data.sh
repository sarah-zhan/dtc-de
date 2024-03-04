set -e

TAXI_TYPE=$1 #"yellow"
YEAR=$2 #2020
URL_PREFIX="https://d37ci6vzurychx.cloudfront.net/trip-data"
for MONTH in {1..12}; do
    MONTH_PADDED=$(printf "%02d" $MONTH)
    URL="${URL_PREFIX}/${TAXI_TYPE}_tripdata_${YEAR}-${MONTH_PADDED}.parquet"

    LOCAL_PREFIX="data/raw/${TAXI_TYPE}/${YEAR}/${MONTH_PADDED}"
    LOCAL_FILE="${TAXI_TYPE}_tripdata_${YEAR}_${MONTH_PADDED}.parquet"
    LOCAL_PATH="${LOCAL_PREFIX}/${LOCAL_FILE}"

    mkdir -p ${LOCAL_PREFIX}
    wget ${URL} -o ${LOCAL_PATH}
done