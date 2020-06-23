# EXO Investing

## Index

- [API V1 doc](docs/api/v1/exo_currency.md) 
- [Backoffice doc](docs/backoffice.md) 
- [Next steps](docs/next-steps.md) 

## Prerequisites
- [Docker](https://docs.docker.com/docker-for-mac/install/) 

## 1. How to run the app?
```bash
docker-compose up
```
This command will expose the app under `http://localhost:8000/`

Also, the first time, `docker-compose` will run the migrations and run the commands to populate the database. 

## 2. How to enter to the container?
After the previous step.

```bash
docker-compose exec app sh
```

## 3. How to run tests?
Once inside the container:
```bash
python manage.py tests
```

## 4. How to run flake8?
Once inside the container:
```bash
flake8
```

## 5. How to run the django commands?
Once inside the container:
```bash
python manage.py [command_name]
```