# PortfolioForge

PortfolioForge is a Django portfolio builder and template library. It lets people choose a portfolio design, enter their profile and project information, preview the result, and export a portfolio as HTML.

The catalog currently contains 34 active templates. Templates live in [`templates/portfolio_templates/`](templates/portfolio_templates/), and each preview is available through:

```text
/api/template/<template-id>/preview/
```

## Local development

Requirements: Python 3.11 and a virtual environment.

```bash
git clone https://github.com/AdeelMalik22/portfolio_manager.git
cd portfolio_manager
python3.11 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py load_templates
.venv/bin/python manage.py runserver 8000
```

Open `http://127.0.0.1:8000/` for the app or `/gallery/` for the template library.

## Tests

```bash
.venv/bin/python manage.py test portfolio.tests -v 1
```

The preview suite checks the complete sample profile, draft previews, template visibility, responsive layout contracts, and independent template structures.

## Useful commands

```bash
# Refresh the active template catalog
.venv/bin/python manage.py load_templates

# Generate preview images for the catalog
.venv/bin/python manage.py generate_template_preview_pack

# Check Django configuration
.venv/bin/python manage.py check
```

## Environment variables

Production deployments should provide:

```text
SECRET_KEY=<long-random-secret>
DEBUG=False
DATABASE_URL=<PostgreSQL connection URL>
```

The project uses SQLite by default for local development and `DATABASE_URL` when a hosted database is configured. Static files are collected into `staticfiles/` and served with WhiteNoise.

## Railway deployment

Connect the GitHub repository to a Railway service and set the watched branch to `master`. Configure these commands in the service if Railway does not detect them automatically:

```text
Build:  pip install -r requirements.txt && python manage.py collectstatic --noinput
Start:  gunicorn portfolio_manager.wsgi --bind 0.0.0.0:$PORT
```

Run migrations and load the catalog after the first deploy:

```bash
python manage.py migrate
python manage.py load_templates
```

Railway deploys are triggered by pushes to the branch configured in the service. A push to another branch, a disconnected GitHub service, paused deployments, or an unchanged commit will not create a new deployment.

## Project layout

```text
portfolio/                  Django application, models, views, services, tests
portfolio_manager/          Django project settings and WSGI/ASGI entrypoints
templates/                  Site pages and portfolio templates
documentation/              Extended project documentation
scripts/                    Development and image-processing utilities
```
