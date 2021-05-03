# Yalantis test task
## Description
This is the test web application for Yalantis python school
Application is the simple CRUD api for course that contains:
- id
- title
- number of classes
- start date
- end date

## Used
- Flask
- SQLAlchemy
- Flask-restful
- Flask swagger ui
- Docker and Docker-compose

## Development environment

Install [poetry](https://python-poetry.org/)
```shell
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

Install dependencies
```shell
poetry install
```

Install pre commit hooks:
```shell
pre-commit install
```

## Production environment

Install [docker](https://docs.docker.com/engine/install/) and [docker-compose](https://docs.docker.com/compose/install/)

Create file ```course_application.env``` inside ```docker``` directory with content:
```shell
FLASK_SECRET_KEY = still-no-secret
DATABASE_PATH = sqlite:////database/database.db
```

Run from the docker dicrectory:
```shell
docker-compose up --build -d
```
It makes two docker containers:
- course_application - contains app
- course_proxy_server - the proxy server

Web application is available on ```http://localhost```

## Routes
The application has 6 routes:
- /swagger - swagger ui documentation
- /api/get_all_courses - endpoint for getting all courses
- /api/get_course - endpoint for getting course by id
- /api/delete_course - endpoint for deleting course by id
- /api/add_course - endpoint for adding new course
- /api/filter_courses - endpoint for filtering courses
