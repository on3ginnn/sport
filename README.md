# Django project

## DREAM TEAM №3 [miro dashboard](https://miro.com/app/board/uXjVKYQfGw4=/)

[![pipeline status](https://gitlab.crja72.ru/django/2024/spring/course/projects/team-3/badges/main/pipeline.svg)](https://gitlab.crja72.ru/django/2024/spring/course/projects/team-3/-/commits/main)

### Prerequisites

1. Install Python:3.10
    * download link

    ```url
    https://www.python.org/downloads/release/python-3100/
    ```

2. Create virtual environment
    * python

    ```bash
    python -m venv venv
    ```

3. Activate virtual environment
    * windows

    ```bash
    .\venv\Scripts\activate
    ```

    * linux

    ```bash
    source venv/bin/activate
    ```

4. Upgrade pip
    * python

    ```bash
    python -m pip install --upgrade pip
    ```

### Installation

1. Clone the repo

   ```bash
   git clone git@gitlab.crja72.ru:django/2024/spring/course/projects/team-3.git
   ```

2. Install requirements
    * production

    ```bash
    pip install -r requirements/prod.txt
    ```

    * test

    ```bash
    pip install -r requirements/test.txt
    ```

    * development

    ```bash
    pip install -r requirements/dev.txt
    ```

3. Use your configuration in .env.example
    * windows

    ```bash
    copy .env.example .env
    ```

    * linux

    ```bash
    cp .env.example .env
    ```

4. Migrate db.sqllite3
    * python

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

### Postgres installation

1. Installation
    * linux

    ```bash
    sudo apt install libpq-dev postgresql postgresql-contrib
    ```

    * windows(Install PostgreSQL)

    ```url
    https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
    ```  

2. Postgres interactive line
    * linux

    ```bash
    sudo -u postgres psql
    ```

    * windows

    ```bash
    run SQL Shell (psql)
    ```  

    If problem with encoding:  

    ```bash
    psql \! chcp 1251
    ```

3. Create DB
    * postgres

    ```bash
    CREATE DATABASE myproject;
    ```

4. Create DB_USER
    * postgres

    ```bash
    CREATE USER myprojectuser WITH PASSWORD 'password';
    GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;
    ```

5. DB setup
    * postgres (windows and linux)

    ```bash
    ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
    ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
    ALTER ROLE myprojectuser SET timezone TO 'UTC';
    ```

    * postgres (in windows)

    ```bash
    \c myproject
    GRANT ALL ON schema public TO myprojectuser;
    ```  

### Static collection

* python

    ```bash
    python manage.py collectstatic
    ```

### Celery
1. Install Erlang
    * windows

    [download and install latest version](https://www.erlang.org/downloads)

2. Install RabbitMQ
    * linux

    ```bash
    sudo apt install rabbitmq-server
    ```

    * windows

    [download and install latest version](https://www.rabbitmq.com/docs/install-windows#downloads)

    ```bash
    run this by double-click: \*:\\\*\\rabbitmq_server-\*.\*.\*\\sbin\\rabbitmq-server.bat
    ```

3. Run celery worker
    * linux

    ```bash
    cd project
    python -m celery -A project worker
    ```

    * windows

    ```bash
    cd project
    celery -A project worker -l info --pool=solo
    ```

### Start

* production

    ```bash
    сd project
    python manage.py runserver
    ```

* test

    ```bash
    сd project
    python manage.py test
    ```
