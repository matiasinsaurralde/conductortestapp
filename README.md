conductortestapp
==

## Run

To run locally (where `APP_JWT_SECRET` is the JWT secret to be used by the auth middleware):

```
$ APP_JWT_SECRET=sekret gunicorn main:app
```

## Tests

To run tests:

```
$ python3 -m pytest
```