# Threat modelling system ( Implementation of practical part of graduate thesis )

## Install
1) Create server/.env file

```
* SECRET_KEY=
* POSTGRES_DB=
* POSTGRES_USER=
* POSTGRES_PASSWORD=
* POSTGRES_PORT=
* POSTGRES_HOST=
* DEBUG=
```
2) Build images
```
make build
```
3) Run project
```
make run
```
4) Apply migrations
```
make migrate 
```
5) Init database with data presets from directory ```init_db_scripts``` (If requiered)

6) Run production
```
make prod
```

