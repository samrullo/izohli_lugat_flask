# Flask on docker
This application demonstrates how we can run python flask application on docker.
Essentially we run our flask application on nginx web server.
The image ```tiangolo/uwsgi-nginx-flask:python3.8-alpine``` serves from ```/app``` folder.
Therefore we mount our current directory to /app in our ```docker-compose.yml``` file.

# docker-compose.yml
docker-compose.yml file looks like below.
I had difficulties getting it right.
For instance, if you don't have a white space after first word ```version``` docker-compose fails to read it.

# sqlite
Initially ```docker-compose build``` was failing to install python libraries such as Flask-SQLAlchemy.
After adding below line to Dockerfile it worked. Apparently below line was installing important linux 
libraries like gcc, which is necessary to successfully install python flask sqlalchemy or its dependencies
like greenlat

```
RUN apk add build-base
```

Finally one issue I was facing, which was purely related to how Flask-SQLAlchemy ```create_all()``` works.
Apparently it only creates tables, if the blueprints or modules that use that table are imported or registered
first.

# postgresql
Just by adding following lines to docker-compose.yml we can launch postgresql container on the same network
and have our flask application container connect to it
```
postgres:
        container_name: 'postgres'
        image: postgres
        environment:
            POSTGRES_USER: root
            POSTGRES_PASSWORD: password
            POSTGRES_DB: flaskdb
        networks:
            - flask-networks
```

But this required to install postgresql-dev package on flask container

```
RUN apk add build-base postgresql-dev
```

Connection string looks like below

```
PROD_DATABASE_URI: postgresql://root:password@postgres:5432/flaskdb
```

When mounting db_data volume flask was trying to connect to postgres before it is ready to accept connections
To resolve it I had to follow stackflow https://stackoverflow.com/questions/35069027/docker-wait-for-postgresql-to-be-running
And add following lines to docker-compose.yml

```
depends_on:
            postgres:
                condition: service_healthy

healthcheck:
            test: ["CMD-SHELL", "pg_isready -U root -d flaskdb"]
            interval: 5s
            timeout: 5s
            retries: 5
```