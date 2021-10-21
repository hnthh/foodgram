# Foodgram-app backend 🍲

Anya Agarenko's [Yandex Practicum](https://practicum.yandex.com) graduation project as a python developer.

[![codecov](https://codecov.io/gh/hnthh/foodgram-project-react/branch/main/graph/badge.svg?token=VH4S1CCXHK)](https://codecov.io/gh/hnthh/foodgram-project-react)
[![Foodgram-app workflow](https://github.com/hnthh/foodgram-project-react/actions/workflows/workflow.yml/badge.svg)](https://github.com/hnthh/foodgram-project-react/actions/workflows/workflow.yml)

> **Foodgram** is an app where users **can**:
> 1) Share their recipes.
> 2) Add recipes to purchases to get a complete list of what they need to buy to prepare dishes, ready for download, [see an example](https://github.com/hnthh/foodgram-project-react/blob/main/shopping-list-example.png).

## Configuration

Configuration is stored in `infra/.env`. For examples see `infra/.env.example`.

## Development setup

Install requirements:
```
python -m pip install pip-tools
make deps
```
```
./manage.py migrate
./manage.py createsuperuser
```

Load initial data:
```
./manage.py load_ingredients
./manage.py create_tags
```

Testing:
```
make test
```

Style checking:
```
make lint
```

Run django development server:
```
./manage.py runserver
```

## After deploy via GitHub actions

The project is available at `http://{HOST}/`.

Go to `http://{HOST}/admin/`, log in as a superuser and make sure that the data was uploaded to the database.

## Foodgram available pages

[http://hnthh.ml/](http://hnthh.ml/) — Home page.

## Thankfulnesss

I really took **a lot** of code snippets from the [Fedor Borshev's](https://github.com/f213) open repositories. You should visit the repositories [https://github.com/fandsdev/django](https://github.com/fandsdev/django) or [https://github.com/tough-dev-school/education-backend](https://github.com/tough-dev-school/education-backend) if you haven't visited them yet. 🐍✨

## Meta

Anya — [https://github.com/hnthh](https://github.com/hnthh) — [anyaagarenko@gmail.com](anyaagarenko@gmail.com)

Distributed under the MIT license. See `LICENSE` for more information.