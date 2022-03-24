# Introduction


## Note:
These instructions are tested on a Mac M1. Shouldn't be that different on Linux. If you're on Windows, I'm sorry, but I have no idea how you can setup your environment. Google will be your friend.

# Local Setup
## Prerequisites
1. PSQL server running
2. Redis server running
3. Python 3.8: `brew install python@3.8`
4. Flak 8 installed: `brew install flake8`
5. Black installed: `brew install black`
6. GDAL installed: `brew install gdal`
6. PROJ installed: `brew install proj`
6. postgis installed: `brew install postgis`

## Config
1. Copy `.env.local.example` and rename it to `.env.local`
2. Update the env variables to match your local config
3. Copy the file `pre-push` to `.git/hooks/pre-push` : `cp pre-push .git/hooks/pre-push`

## Setup local DB
Install PSQL spatial extension
https://docs.djangoproject.com/fr/3.2/ref/contrib/gis/install/postgis/

Setup DB user:

ALTER ROLE localuser SET client_encoding TO 'utf8';
ALTER ROLE localuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE localuser SET timezone TO 'UTC';

Grant privileges to local DB user:

GRANT ALL PRIVILEGES ON DATABASE estimer TO localuser;

## Setup local env
1. Create a virtual environment
at `/estimer`
   ```bash
   python3.9 -m venv venv
   ```
2. Activate the virtual environment
   ```bash
   source venv/bin/activate
   ```
3. Install dependencies
    ```bash
   pip install -r requirements/local.txt
   ```
4. Import dvf data to your local DB
   ```bash
   python manage.py shell
   ```
   ```python
   from src.dvf.aggregator.data_import import import_data
   for year in range(2016,2021):
      import_data(year)
   ```
5. Import iris data to your local DB
   ```bash
   python manage.py shell
   ```
   ```python
   from src.iris.aggregator.data_import import import_data
   import_data(2021)
   ```
6. Fill `geometry_4326` column in your database
   From a psql prompt:
   ```sql
   UPDATE iris_iris SET "geometry_4326" = ST_Transform(geometry,4326)
   ```

# Prod setup
TODO: add prod setup guide
