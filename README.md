# Mailing list app

## Setup

The first thing to do is to clone the repository:

```shell
https://gitlab.com/testtask8/Notification.git
cd Notification
```

Create a virtual environment to install dependencies in and activate it:

```shell
py -m venv notifEnv
notifEnv\Scripts\active
```

Then install the dependencies:

```shell
(notifEnv) pip install -r requirements.txt 
```

Note the `(notifEnv)` in front of the prompt.
This indicates that this terminal session operates in a virtual environment set.

Once `pip` has finished downloading the dependencies.
Go to the root directory and run migration:

```shell
cd notifications
python manage.py migrate
```

After `migrate` command, we need setup `.env` file in `core` directory.
This directory also contains an example of a completed .env file.

Now we can run project:

```shell
python manage.py runserver
python -m celery -A core worker -l info -P eventlet
celery -A core beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

Note that `eventlet` params specific only for Windows system.

Note that you have to run `redis-server` yourself by specifying
`port` and `host` in the `.env` file.

And navigate to `http://127.0.0.1:8000/docs/`.

## Additional tasks

#### The following additional tasks were performed:

* Organize testing code. (Step 1)
* To open the page with Swagger UI at `/docs/` and display the description of the developed API. (Step 5) 
* Implement an additional service that once a day sends statistics on processed mailings to email. (Step 8)




