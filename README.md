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