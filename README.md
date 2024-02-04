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

## Google Cloud set up
- Go to .ssh folder -> `ssh-keygen -t rsa -f your-file-name -C cloud-username -b 2048`
- you can leave the password as empty
- you will have a private and public key in .ssh folder
- put the public key (xx.pub) to google cloud
- Compute Engine -> settings -> metadata -> SSH KEYS -> ADD -> (in terminal) cat xx.pub -> copy the info and paste the key in google cloud -> save
- VM instances -> create a new instance -> pick your configuration
- remember the External IP
- `ssh -i ~/.ssh/keyname username@External IP`
- use `htop` to check the machines; `F10` exit
- `gcloud --version` check google cloud info
- we can create a config file to login gl
  - config file
    ```python
    Host vm instance name
    HostName your-gl-external-ip
    User gl-username
    IdentityFile ~/.ssh/key-name
    ```

## install ananconda
- download from https://www.anaconda.com/download -> choose your own installer -> right click, copy link
- for Linux `wget https://repo.anaconda.com/archive/Anaconda3-2023.09-0-Linux-x86_64.sh`
- press "enter" until it asks you to accept the license -> "yes" -> "yes" initialize anaconda
- `ssh de-zoomcamp` to login
- `ctrl+d` to logout

## install docker
```python
sudo apt-get update
sudo apt-get install docker.io
```

## connect to remote-shh
- vscode install Remote-SSH extension
- F1 KEY -> Add new host -> de-zoomcamp (you might need to adjust your config file if there is a connection issue)
- every time you restart the server, the external IP may change

## docker without sudo
https://github.com/sindresorhus/guides/blob/main/docker-without-sudo.md
- Add the docker group if it doesn't already exist `sudo groupadd docker`
- Add the connected user $USER to the docker group `sudo gpasswd -a $USER docker`
- Restart the docker daemon `sudo service docker restart`
- Test whether it works -> `docker run hello-world`

## docker-compose in gc
https://github.com/docker/compose/releases/download/v2.24.1/docker-compose-linux-x86_64
- make a folder bin
- in bin folder install docker-compose
- `wget https://github.com/docker/compose/releases/download/v2.24.1/docker-compose-linux-x86_64`
- make it executable `chmod +x docker-compose`
- make it visible to any directories `nano .bashrc`
- at the end of the document add `export PATH="${HOME}/bin:${PATH}"`
- `ctrl + o` to save the file
- `ctrl + x` to exit
- download `git clone https://github.com/sarah-zhan/dtc-de.git`
- `docker network create pg-network` (optional, if the yaml returns error)
- run yaml file `docker-compose up -d`

## forward the port to local
- show vscode terminal -> "PORTS" -> forward Port
- access database `pgcli -h localhost -u labber -d ny_taxi`
- add port 8080 -> localhost:8080 -> login pgadmin

## run upload_data
- jupyter notebook
- copy the link localhost:8888..... in the browser (can also do it in vscode)
- test to insert 100 rows of data
- try whether it works `pgcli -h localhost -u labber -d ny_taxi`
- `dt`

## download terraform
- download `wget https://releases.hashicorp.com/terraform/1.7.0/terraform_1.7.0_linux_amd64.zip`
- `unzip terraform_1.7.0_linux_amd64.zip`
- `rm terraform_1.7.0_linux_amd64.zip`

## Configure Terraform
- main.tf
```python
terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "5.12.0"
    }
  }
}

provider "google" {
  project     = "my-project-id"
  region      = "us-central1"
}

resource "google_storage_bucket" "zoomcamp_bucket" {
  name          = "terraform-bucket-01" # this name must be globaly unique
  location      = "US"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "demo" {
  dataset_id                      = "demo_dataset"
  default_partition_expiration_ms = 2592000000  # 30 days
  default_table_expiration_ms     = 31536000000 # 365 days
  description                     = "demo dataset"
  location                        = "US"
  max_time_travel_hours           = 96 # 4 days

}
```

## Terraform
- sudo snap install terraform --classic
- terraform init (after terraform, provider block in main.tf)
- terraform plan (after resource block in main.tf)
- terraform apply
- terraform destroy (delete resources)

## add variables.tf
for example
```python
variable "dataset_name" {
  type = string
  default = "demo_dataset"
  description = "value of the demo dataset"
}
```
**make sure to update .gitignore file to include terreform info**

## add credential - transfer files
- `sudo apt-get install openssh-server`
- in ssh__config add `Subsystem sftp internal-sftp`
- generate ssh key `ssh-keygen -t rsa -b 2048 -f ~/.ssh/id_rsa -C "your_email@example.com"`
- add the key to gl `gcloud compute instances add-metadata INSTANCE_NAME --metadata ssh-keys="USERNAME:$(cat ~/.ssh/id_rsa.pub)"`
- export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/key-file.json
- Create a Service Account in the console (IAM)
- Create and Download JSON Key File: "IAM & Admin" > "Service accounts," select your service account, and click on "Create Key." Choose JSON as the key type and download the key file.
- Set the Environment Variable: `export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/key-file.json`
- Verify the Configuration: `echo $GOOGLE_APPLICATION_CREDENTIALS`
- Use the gcloud SDK with the Service Account: `gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS`
- `mkdir -p ~/.ssh` (optional)
- `chmod 700 ~/.ssh` (optional)
- `touch ~/.ssh/authorized_keys`
- `chmod 600 ~/.ssh/authorized_keys`
- `echo "your_public_key" >> ~/.ssh/authorized_keys`
- `sftp username@external_ip` / `sftp instance_name` SFTP (Secure File Transfer Protocol) is a secure alternative to FTP for transferring files.
- create a folder -> cd to that folder
- send the file to that folder `put local_file.txt`
- download fild `get remote_file.txt`
- `exit` for exit

## Google Cloud
- Set the Environment Variable: `export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/key-file.json`
- Use the gcloud SDK with the Service Account: `gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS`
- remove credential `unset GOOGLE_APPLICATION_CREDENTIALS`


# Week2 Workflow Orchestration
- Install docker
```python
#clone the repo
git clone https://github.com/mage-ai/mage-zoomcamp.git mage-zoomcamp

# navigate to folder
cd mage-zoomcamp

# check the files inside folder
ls -la

# change the name
mv dev.env .env

# build the container
docker compose build

# update the docker
docker pull mageai/mageai:latest

# start the container
docker compose up

# navigate to http://localhost:6789 in your browser!

![mage_interface](./photos/image.png)
```

- update io_config.yaml in mage
  add the code below
  ```python
  dev:
  POSTGRES_CONNECT_TIMEOUT: 10
  POSTGRES_DBNAME: "{{env_var('POSTGRES_DBNAME')}}"
  POSTGRES_SCHEMA: "{{env_var('POSTGRES_SCHEMA')}}"
  POSTGRES_USER: "{{env_var('POSTGRES_USER')}}"
  POSTGRES_PASSWORD: "{{env_var('POSTGRES_PASSWORD')}}"
  POSTGRES_HOST: "{{env_var('POSTGRES_HOST')}}"
  POSTGRES_PORT: "{{env_var('POSTGRES_PORT')}}"
  ```
- Edit pipeline -> new -> standard (batch) -> Edit -> Pipeline settings -> edit the pipeline name
- Edit pipeline -> Data loader -> SQL -> Name(edit it) -> save
- Connection (PostgreSQL) -> Profile (dev) -> choose "Use raw SQL" -> run block
![sqlblock](sqlblock.png)

use different method
- Edit pipeline -> Python -> API -> Name(edit it) -> save
- add url in the template url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz'
- declare deta types
```python
    # declear data type
    taxi_dtypes = {
        'VendorID': pd.Int64Dtype(),
        'passenger_count': pd.Int64Dtype(),
        'trip_distance': float,
        'RatecodeID': pd.Int64Dtype(),
        'store_and_fwd_flag': str,
        'PULocationID': pd.Int64Dtype(),
        'DOLocationID': pd.Int64Dtype(),
        'payment_type': pd.Int64Dtype(),
        'fare_amount': float,
        'extra': float,
        'mta_tax': float,
        'tip_amount': float,
        'tolls_amount': float,
        'improvement_surcharge': float,
        'total_amount': float,
        'congestion_surcharge': float
    }

    # timestamp data
    parse_dates = ['tpep_pickup_datetime', 'tpep_dropoff_datetime']


    return pd.read_csv(url, sep=",", compression="gzip", dtype=taxi_dtypes, parse_dates=parse_dates)
```
![load_api_data](./photos/load_api_data.png)

- transform taxi data
  - TRANSFORMER -> Python -> Generic
  - clean the data that with passenger count is 0
```python
  @transformer
  def transform(data, *args, **kwargs):
      print(f"Preprocessing: rows with zero passengers: {data['passenger_count'].isin([0]).sum()}")

      return data[data['passenger_count'] > 0]
```
  - assertion test
```python
  @test
  def test_output(output, *args) -> None:
      assert output['passenger_count'].isin([0]).sum() == 0, 'There are rides with 0 passengers'
```
![transform_data](transform_data.png)

- export data
  - Data exporter -> Python -> PostgreSQL
  - update the schema name, table name, config_profile
![export_data](./photos/export_data.png)

- quick test
  - Data loader -> SQL
![load_taxi_data_test](./photos/load_taxi_data_test.png)