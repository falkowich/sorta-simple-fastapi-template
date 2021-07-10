 
# FastAPI Sorta Simple Template.

[![python](https://img.shields.io/static/v1?label=python&message=3.9%2B&color=informational&logo=python&logoColor=white)](https://www.python.org/)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
![Continuous Integration and Delivery](https://github.com/falkowich/sorta-simple-fastapi-template/workflows/Github%20Actions/badge.svg?branch=master)

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
docker-compose exec web python app/db.py
```

Apply db migrations

```shell


Tail logs
```shell
docker-compose logs -s
```

#### Testing




 
 
   
 5546   
 5547    
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
