 
# Temporary README :)
 
 
 
 
 
   
 5546  docker-compose build  
 5547  docker-compose up -d  
 5556  docker-compose logs web  
 5559  docker-compose exec web-db   
 5560  docker-compose exec web-db  sh  
 5561  docker-compose exec web-dev sh  
 5562  docker-compose exec web_dev sh  
 5563  docker-compose exec web sh  
 5564  docker-compose down  
 5569  docker-compose down -v+  
 5570  docker-compose down -v  
 5571  docker-compose exec web-db psql -U postgres  
 5573  docker-compose up -d --build  
 5574  docker-compose exec web python app/db.py  
 5576  docker-compose exec web python -m pytest -k ping\n  
 5577  docker-compose exec web python -m pytest  
 5578  docker-compose exec web python -m pytest -p no:warnings  
 5579  docker-compose exec web python -m pytest --durations=2  
 5757  docker-compose pull  
 5758  docker-compose up   
docker-compose exec web  
 3523  docker-compose exec web shell  
 3526  docker-compose exec web python -m pytest --cov="." --cov-report html  
 3533  docker-compose exec web python -m pytest --diff  
 3534  docker-compose exec web python -m pytest   
 3535  docker-compose exec web python -m pytest -v  
 3536  docker-compose exec web python -m pytest --cov="."  
 3538  docker-compose exec web python -m pytest -vv  
 3540  docker-compose exec web pytest -k "unit" -n auto  
 docker-compose exec web python -m pytest -p no:warnings -v  
 2449  docker-compose exec web python -m pytest -p no:warnings -vv  
 2450  docker-compose exec web python -m pytest -k read  
 2451  docker-compose exec web python -m pytest -k "summary and not test_read_summary"  
 2545  docker-compose exec web black . --diff  
 2547  docker-compose exec web /bin/sh -c "isort ./**/*.py --diff"  
 2548  docker-compose exec web black . --check  
 2549  docker-compose exec web /bin/sh -c "isort ./**/*.py --check-only"  
 2760  docker-compose stop  
 2776  docker-compose restart  
  

# Fastapi - readme and ideas from a https://github.com/tobiwankenobii/fastapi-essential and will be customed later on..

[![python](https://img.shields.io/static/v1?label=python&message=3.9%2B&color=informational&logo=python&logoColor=white)](https://www.python.org/)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
![Continuous Integration and Delivery](https://github.com/tobiwankenobii/fastapi-essential/workflows/Github%20Actions/badge.svg?branch=master)

Simple REST Api made using FastAPI framework. It can be used as a very basic CRUD boilerplate, which is fully dockerized
along with PostgreSQL database, uses Tortoise as db ORM with Aerich for migrations, has Pytest, Codecoverage and Black
support and uses Poetry as a dependency manager.

It's quite hard to find fully working and easy to manage FastAPI boiler, which supports modern extensions like Poetry or
Tortoise. I hope this repo will help you achieve that.

## Usage

### Docker setup

Build Docker images

```shell
docker-compose build
```

Run Docker containers

```shell
docker-compose up
```

### Make commands

Apply Tortoise schema

```shell
docker-compose exec fastapi make schema
```

Apply Aerich migrations

```shell
docker-compose exec fastapi make migrations
```

Run tests

```shell
docker-compose exec fastapi make test
```

Run lint

```shell
docker-compose exec fastapi make lint
```

### Removing migrations

If there is a need to remove existing migrations and replace them with some new models, delete the `migrations` folder
and run

```shell
docker-compose exec fastapi aerich init-db
```

If new `aerich.ini` file is needed, delete the existing one and run

```shell
docker-compose exec fastapi aerich init -t src.database.TORTOISE_ORM
```

And apply migrations

```shell
docker-compose exec fastapi aerich upgrade
```
