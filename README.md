# Villotracker

This project provides a minimal Django application along with a client library to interact with the JCDecaux bike sharing API.

## Installation

Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

## Running Django commands

Django commands are executed via `manage.py`. Use `python manage.py <command>` to run any management task. For example, to apply migrations and start the development server:

```bash
python manage.py migrate
python manage.py runserver
```

## SECRET_KEY environment variable

Django requires a secret key for cryptographic signing. Set the `SECRET_KEY`
environment variable before running any Django command:

```bash
export SECRET_KEY="<your secret key>"
```

Alternatively, create a `.env` file in the project root and set `SECRET_KEY`
there so it is loaded automatically.

## API_KEY environment variable

The JCDecaux clients look for an `API_KEY` environment variable. Set it before running the server or scripts so requests to the JCDecaux API are authenticated:

```bash
export API_KEY="<your api key>"
```

You can also add `API_KEY` to the `.env` file alongside `SECRET_KEY`:

```text
SECRET_KEY=<your secret key>
API_KEY=<your api key>
```

The key is automatically used by `JCDecauxClient` when not provided explicitly.

## Using `JCDecauxClient`

Below is a minimal example that lists the available contracts:

```python
from libs.jcdecauxclient import JCDecauxClient

client = JCDecauxClient()  # uses API_KEY from environment
contracts = client.get_contracts()
for c in contracts:
    print(c.name)
```

Running the Django development server after setting `API_KEY` allows the application to access the JCDecaux API if needed:

```bash
export API_KEY="<your api key>"
python manage.py runserver
```
