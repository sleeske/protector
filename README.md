# Django Protector

Welcome to the Django Protector, where you can safely share important links and files.

## Prerequisites

To run this App make sure `Docker` and `docker-compose` (Docker Engine v19.03.0+) are installed on your system.

Create an `.env` file and open it in your editor of choice to provide default values:

```shell
cp .env.example .env
vi .env
```

> Note: for local development/preview with Docker set DATABSE_URL to `postgres://postgres:postgres@postgres:5432/postgres` and ALLOWED_HOSTS to `*`


## Buid & run the app

In project root directory execute:

```shell
docker-compose build
```

Depending on your internet connection either fetch your favourite drink or sit tight, as the initial build might last anywhere between
5 to ∞ minutes.

Assuming the build has finished it's time to run the app:
```shell
docker-compose up
```

The startup should be almost instantaneous. You might also notice that any unapplied migrations are being executed. That's what the `bootstrap` management command takes care of. For your convenience it also tries to create a superuser, when in DEBUG mode. The defaul credentials are `admin`:`test123`.

The home page is available at http://localhost:8000/ and the admin resides at the [/admin](http://localhost:8000/admin).
To make life easier the home page has links to both Form-based views and API views (including statistics endpoint).

The default password for Protected Resource can be changed per-object in the admin.

And that's all folks, have fun exploring both the code and the app! (Although the latter might not be that fun, see [TODOS](#todos) no. 3)

## TODOS
- deploy to Heroku (sorry, really had no time to tackle that one)
- add more test coverage (although I hope that the existing test cases, the setup and the libraries I've used will give you an idea where would that go)
- add styling to the Form-based views.
- improve the error handlng mechanism for API views. It works now, but could've much cleaner.
- and probably many more, which I hope we'll have a chance to discuss ;)
