# FastAPI SortaSimpleTemplate

[![python](https://img.shields.io/static/v1?label=python&message=3.9%2B&color=informational&logo=python&logoColor=white)](https://www.python.org/)
[![Maintainability](https://api.codeclimate.com/v1/badges/1c619a6e8f4de4847464/maintainability)](https://codeclimate.com/github/falkowich/sorta-simple-fastapi-template/maintainability)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![codecov](https://codecov.io/gh/falkowich/sorta-simple-fastapi-template/branch/coverage/graph/badge.svg?token=W4XV5BH66E)](https://codecov.io/gh/falkowich/sorta-simple-fastapi-template)

This repo conatins my own try to learn FastAPI and create a simple template for myself.

It is a fully dockerized dev environment with Tortoise ORM with Aerich for migrations. I strive to use Pytest, Codecoverage and black as code style.  
It's a project in flux, that is changed when new ideas is implemented.

If you have any suggestions or even a code PR, do not hesitate to tell me or submit a PR :)

## How to use

### Docker development images usage

Build dev images

```shell
docker-compose build 
```

Startup dev conatiners

```shell
docker-compose up -d
```

Initiate database

```shell
docker-compose exec web python scripts/manage.py --mode generate-schemas
```

Create first admin user

```shell
docker-compose exec web python scripts/manage.py --mode create-admin
```

Manage db migrations

```shell
docker-compose exec web aerich upgrade

```

More Aerich commands

```shell
downgrade  Downgrade to specified version.
heads      Show current available heads in migrate location.
history    List all migrate items.
init       Init config file and generate root migrate location.
init-db    Generate schema and generate app migrate location.
inspectdb  Introspects the database tables to standard output ...
migrate    Generate migrate changes file.
upgrade    Upgrade to specified version.
```

Tail logs

```shell
docker-compose logs -f
```

#### Testing

Run tests

```shell
docker-compose exec web python -m pytest 
```

Run tests with coverage

```shell
docker-compose exec web python -m pytest --cov="."
```

Run test with html coverage

```shell
docker-compose exec web python -m pytest --cov="." --cov-report html
```

Run tests with xml coverage

```shell
docker-compose exec web python -m pytest --cov="." --cov-report=xml
```

Upload above test to codecov

For this to work you must work in your local virtualenv.

```shell
  cd project
  poetry shell
  codecov -t [token]
```

Run t ests with unittest module

```shell
docker     -compose exec web pytest -k "unit" -n auto  
```

### Code quality

#### Black

Check code

```shell
docker-compose exec web black . --check
```

Show difference

```shell
docker-compose exec web black . --diff
```

Apply changes

```shell
docker-compose exec web black . 
```

#### isort

Check code

```shell
docker-compose exec web /bin/sh -c "isort ./**/*.py --check-only"
```

Show difference

```shell
docker-compose exec web /bin/sh -c "isort ./**/*.py --diff"
```

Apply changes

```shell
docker-compose exec web /bin/sh -c "isort ./**/*.py"
```
