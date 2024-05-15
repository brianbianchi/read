## venv
```
python3 -m venv venv
source venv/bin/activate
deactivate 
```

## django
```
python manage.py createsuperuser
python manage.py makemigration #change schema
python manage.py migrate #apply
python manage.py loaddata urls #from /fixtures/urls.py
```

## docker
```
docker build -t read .
docker run -p 8000:8000 read
docker-compose up -d
docker exec -it [[CONTAINER_ID]] [[COMMAND]]
```
