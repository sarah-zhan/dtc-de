# Week1 Set up the environment

## postgres docker
```python
docker run -it \
-e POSTGRES_USER="labber" \
-e POSTGRES_PASSWORD="labber" \
-e POSTGRES_DB="ny_taxi" \
-v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
-p 5432:5432 \
--network=pg-network \
--name pg-database \
postgres:13
```

## pgcli access to database
```python
pgcli -h localhost -p 5432 -u labber -d ny_taxi
```

## inject data (upload_data.ipynb)
- can create a ipynb in vscode
- or use jupyter notebook in the browser
 - if cannot open jupyter notebook in the browser, try the code below
 `sudo update-alternatives --install /usr/bin/x-www-browser x-www-browser /opt/google/chrome/google-chrome 200`
- follow the steps in upload_data.ipynb

## pgadmin
```python
docker run -it \
-e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
-e PGADMIN_DEFAULT_PASSWORD="labber" \
-p 8080:80 \
--network=pg-network \
--name pgadmin \
dpage/pgadmin4
```

## create pg network to connect pgadmin and postgres
```python
docker network create pg-network
```
**In the pgAdmin interface**
- create a new server
- input the name in general
- Connection:
    - host name: pg-database
    - username: labber
    - password: labber

- interface
    - Database
        - ny_taxi
            - schemas
                - tables
                    - yellow_taxi_data

- tools -> query tool -> write your own query

## conver jupyter notebook to script
```python
jupyter nbconvert --to=script upload_data.ipynb
```

## Ingest data with the script
```python
url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"
python3 ingest_data.py \
    --user=labber \
    --password=labber \
    --host=localhost \
    --port=5432 \
    --database=ny_taxi \
    --table=yellow_taxi_trips \
    --url=${url}
```
## Dockerfile
```python
FROM python:3.10

RUN apt-get install wget
RUN pip install pandas sqlalchemy pgcli psycopg2-binary

WORKDIR /app
COPY ingest_data.py ingest_data.py

ENTRYPOINT [ "python3", "ingest_data.py" ]
```
```python
docker build -t taxi_ingest:v001 .

# user ifconfig to find the IP address -- under "eth0"
# can run python -m http:server to make the ingestion faster
python3 -m http.server 8000

url="http://172.23.55.174:8000/yellow_tripdata_2021-01.csv.gz"
docker run -it \
    --network=pg-network \
    taxi_ingest:v001 \
        --user=labber \
        --password=labber \
        --host=pg-database \
        --port=5432 \
        --database=ny_taxi \
        --table=yellow_taxi_trips \
        --url=${url}
```

## Docker-compose to build connection and inject data
- intall
```python
# Download the Docker Compose binary
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Apply executable permissions to the binary
sudo chmod +x /usr/local/bin/docker-compose

# Verify the installation
docker-compose --version
```
- yaml file
```python
services:
  pgdatabase:
    image: postgres:13
    environment:
      - POSTGRES_USER=labber
      - POSTGRES_PASSWORD=labber
      - POSTGRES_DB=ny_taxi
    ports:
      - "5432:5432"
    volumes:
      - ./ny_taxi_postgres_data:/var/lib/postgresql/data:rw
    networks:
      - pg-network
  pgadmin:
    image: dpage/pgadmin4
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@admin.com
      - PGADMIN_DEFAULT_PASSWORD=labber
    ports:
      - "8080:80"
    networks:
      - pg-network
networks:
  pg-network:
    name: pg-network
    external: true
```
- run yaml
```python
docker-compose up -d
```
- stop yaml
```python
docker-compose down
```