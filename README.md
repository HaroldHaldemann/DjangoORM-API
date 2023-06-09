# Introduction

The application enables users to create and update a customer database, create and track contracts and events.
The endpoints of this API and their usage are described in the [Postman documentation](https://documenter.getpostman.com/view/25447803/2s93sc3Xtn)
Here is the [ERD](./erd_epicevents.png) (entity-relation diagram) we used for model implementation.

# Documentation

## Prerequisites

- Python 3.6 or higher
- Postgresql

## Installation

1 - Clone the github Repository.

```bash
git clone https://github.com/HaroldHaldemann/DjangoREST-API
```

2 - Create your virtual environment.

```bash
python -m venv name-virtual-env
```

3 - Activate your virtual environment.

On Windows
```windows
name-virtual-env\Scripts\activate.bat #In cmd
name-virtual-env\Scripts\Activate.ps1 #In Powershell
```

NB: If you activate your environment with Powershell, don't forget to enable running script :
```windows
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser
```

On Unix/MacOs
```bash
source name-virtual-env/bin/activate
```

4 - Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required modules.

```bash
pip install -r ./requirements.txt
```

5 - Create a database with SQL shell (psql)
```sql
CREATE DATABASE epic_events;
```

5 - Make the migrations for Django to enable the database
```bash
python ./manage.py makemigrations
python ./manage.py migrate
```

## Usage
Before running the app, you will need some environment varibles, just execute:
```bash
python ./setup_env.py
```
Fill the information asked with your own.

To run this application, execute the following command to launch the local server:
```bash
python ./manage.py runserver
```

The server will be available at http://127.0.0.1:8000/
The admin site will be available at http://127.0.0.1:8000/admin/

Every endpoints and their documentation are available in the [Postman documentation](https://documenter.getpostman.com/view/25447803/2s93sc3Xtn)

To create a super user (admin), just execute:
```bash
python ./manage.py createsuperuser
```

## Logging

The API stocks the errors and exceptions in the file [errors.log](errors.log).

## Tests

To run the tests, just execute: 
```bash
coverage run ./manage.py test
```

You can then have the coverage report with:
```bash
coverage report
```