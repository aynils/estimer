# Introduction


## Note:
These instructions are tested on a Mac M1. Shouldn't be that different on Linux. If you're on Windows, I'm sorry, but I have no idea how you can setup your environment. Google will be your friend.

# Local Setup
## Prerequisites
1. PSQL server running
2. Redis server running
3. Python 3.9: `brew install python@3.9`
4. Flak8 installed: `brew install flake8`
5. Black installed: `brew install black`

## Config
1. Copy `.env.local.example` and rename it to `.env.local`
2. Update the env variables to match your local config
3. Copy the file `pre-push` to `.git/hooks/pre-push` : `cp pre-push .git/hooks/pre-push`

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
   pip install -r requirements.txt 
   ```
4. Import data to your local DB
   ```bash
   python manage.py shell
   ```
   ```python
   from dvf.aggregator.data_import import import_data
   for year in range(2016,2021):
      import_data(year)
   ```

Setup DB user:

ALTER ROLE localuser SET client_encoding TO 'utf8';
ALTER ROLE localuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE localuser SET timezone TO 'UTC';

Grant privileges to local DB user:

GRANT ALL PRIVILEGES ON DATABASE XXXXX TO localuser;

# Prod setup
TODO: add prod setup guide
