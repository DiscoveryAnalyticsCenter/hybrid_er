# Hybrid Entity Resolution

Hybrid entity resolution interface.


## Setting Up Your Users

To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command:

```
$ docker-compose -f local.yml run --rm django python manage.py createsuperuser
```

## Load data

Clusters with keys as entities/text and values as cluster integers.

```
docker-compose -f local.yml run --rm django python manage.py populate_clusters data/clusters.json
```


Scores with columns entity, entity from a cluster, score.

```
docker-compose -f local.yml run --rm django python manage.py populate_scores data/scores.csv
```


## Run server

Set environment in .envs/.local

```
$ docker-compose -f local.yml up
```


For detailed deployment see [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html)
