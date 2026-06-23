# Property Management System

A Dockerized Django vacation rental property search project using PostgreSQL, PostGIS, and pgvector.

The project supports:

- Vacation rental property listing
- Homepage search form
- Location-based property search
- Location autocomplete API
- Property listing page with pagination
- Property detail page with image gallery, amenities, and distance from city
- Django Admin dashboard for properties, locations, and property images
- CSV property import
- Location embeddings for semantic location search

---

## Tech Stack

- Python 3.13
- Django 6
- Django GIS
- PostgreSQL 18
- PostGIS
- pgvector
- Django REST Framework
- django-filter
- pandas
- sentence-transformers
- Docker and Docker Compose

---

## Project Structure

```text
property-management-system-rangon/
├── core/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── docker/
│   ├── django/
│   │   └── Dockerfile
│   └── postgres/
│       ├── Dockerfile
│       └── init.sql
├── property_app/
│   ├── management/
│   │   └── commands/
│   │       ├── import_properties.py
│   │       └── generate_embeddings.py
│   ├── static/
│   │   └── property_app/
│   │       ├── css/site.css
│   │       └── js/script.js
│   ├── templates/
│   │   └── property_app/
│   │       ├── partials/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── property_list.html
│   │       └── property_detail.html
│   ├── admin.py
│   ├── embeddings.py
│   ├── models.py
│   ├── search.py
│   ├── urls.py
│   └── views.py
├── docker-compose.yml
├── manage.py
├── requirements.txt
└── README.md
```

---

## Prerequisites

Install these before running the project:

- Docker
- Docker Compose
- Git

For macOS, make sure Docker Desktop is running before using `docker compose`.

For Ubuntu, make sure your user can run Docker commands without `sudo` if your environment does not allow sudo access.

---

## Environment Setup

Create a `.env` file in the project root.

```bash
cp .env.example .env
```

If `.env.example` is not available, create `.env` manually:

```env
DJANGO_SECRET_KEY=change-this-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

POSTGRES_DB=property_db
POSTGRES_USER=property_user
POSTGRES_PASSWORD=property_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

Notes:

- `POSTGRES_HOST=db` is correct when Django runs inside Docker Compose.
- If you run Django directly on your host machine, use `POSTGRES_HOST=localhost` instead.
- Keep `DJANGO_DEBUG=True` only for local development.

---

## Build the Docker Images

From the project root, run:

```bash
docker compose build
```

This builds:

- the Django web image with GIS dependencies such as GDAL, GEOS, and PROJ
- the PostgreSQL image with PostGIS and pgvector enabled

---

## Start the Project

Run:

```bash
docker compose up -d
```

Check running containers:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs -f web
```

For database logs:

```bash
docker compose logs -f db
```

---

## Run Database Migrations

After the containers are running, create and apply migrations:

```bash
docker compose exec web python manage.py makemigrations
```

```bash
docker compose exec web python manage.py migrate
```

The database image runs `docker/postgres/init.sql` during first database initialization. That file enables:

```sql
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS vector;
```

---

## Create an Admin User

Create a Django superuser:

```bash
docker compose exec web python manage.py createsuperuser
```

Then open the admin panel:

```text
http://localhost:8000/admin/
```

---

## Import Properties from CSV

Place your CSV file inside the project, for example:

```text
data/properties.csv
```

Then run:

```bash
docker compose exec web python manage.py import_properties data/properties.csv
```

### Expected CSV Columns

The import command expects these columns:

```text
city
state
country
location_latitude
location_longitude
property_latitude
property_longitude
title
description
property_type
status
price
bedrooms
bathrooms
amenities
primary_image_url
image_urls
image_captions
```

Example row:

```csv
city,state,country,location_latitude,location_longitude,property_latitude,property_longitude,title,description,property_type,status,price,bedrooms,bathrooms,amenities,primary_image_url,image_urls,image_captions
Destin,Florida,USA,30.3935,-86.4958,30.3901,-86.4972,Beachfront Villa,Spacious villa near the beach,villa,available,350,4,3,"WiFi, Pool, Kitchen",https://example.com/main.jpg,"https://example.com/1.jpg|https://example.com/2.jpg","Front view|Living room"
```

Notes:

- `image_urls` should use `|` to separate multiple image URLs.
- `image_captions` should also use `|` in the same order as `image_urls`.
- The command uses `get_or_create`, so rerunning the import will not update existing properties with the same generated slug.

---

## Generate Location Embeddings

Location embeddings are generated when a `Location` is saved.

To regenerate embeddings for all existing locations, run:

```bash
docker compose exec web python manage.py generate_embeddings
```

The embedding model used by the project is:

```text
all-MiniLM-L6-v2
```

The first run needs access to download the model if it is not already cached inside the container.

---

## Run the Development Server

The Django container starts the server automatically using:

```bash
python manage.py runserver 0.0.0.0:8000
```

Open the site:

```text
http://localhost:8000/
```

Useful routes:

```text
/                              Homepage
/properties/                   Property listing page
/properties/?q=Destin          Search by location
/properties/?q=Destin&sort=price_asc
/properties/<slug>/            Property detail page
/api/locations/autocomplete/?q=de
/admin/                        Django Admin
```

---

## Main Features

### Homepage

The homepage shows:

- search form
- autocomplete-enabled location input
- featured available properties

Featured properties are selected from properties with:

```python
status="available"
```

### Property Listing Page

The listing page supports:

- location search
- semantic fallback search
- pagination
- sorting by newest, price low to high, and price high to low

### Property Detail Page

The detail page shows:

- property title
- location
- property type
- bedrooms and bathrooms
- image gallery
- description
- amenities
- nightly price
- distance from property point to city/location point

### Location Autocomplete API

Endpoint:

```text
/api/locations/autocomplete/?q=<query>
```

Example:

```text
/api/locations/autocomplete/?q=des
```

The API returns matching locations as JSON.

---

## Admin Dashboard

The Django Admin supports:

- managing locations
- managing properties
- managing property images
- inline property image upload/editing from the property page
- image preview in admin
- filters for property type, status, bedrooms, country, state, and city
- search by title, description, location name, city, state, and country

Admin URL:

```text
http://localhost:8000/admin/
```

---

## Static and Media Files

Static files are stored in:

```text
property_app/static/property_app/
```

Templates are stored in:

```text
property_app/templates/property_app/
```

Uploaded media files are served from:

```text
media/
```

In local development, media files are served only when `DEBUG=True`.

---

## Common Commands

### Build images

```bash
docker compose build
```

### Start containers

```bash
docker compose up -d
```

### Stop containers

```bash
docker compose down
```

### Stop containers and remove database volume

Use this only when you want to reset the database completely:

```bash
docker compose down -v
```

### Run migrations

```bash
docker compose exec web python manage.py migrate
```

### Create migrations

```bash
docker compose exec web python manage.py makemigrations
```

### Create superuser

```bash
docker compose exec web python manage.py createsuperuser
```

### Import CSV data

```bash
docker compose exec web python manage.py import_properties data/properties.csv
```

### Regenerate embeddings

```bash
docker compose exec web python manage.py generate_embeddings
```

### Open Django shell

```bash
docker compose exec web python manage.py shell
```

### Run tests

```bash
docker compose exec web python manage.py test
```

---

## Working on macOS and Ubuntu

This project is intended to run on both:

- macOS Apple Silicon machines
- Ubuntu Intel machines

The Dockerfiles use:

```dockerfile
FROM --platform=$TARGETPLATFORM ...
```

So Docker should build the correct image for the current machine architecture.

If you generate new files from inside Docker and want to avoid root-owned files on the host, use:

```bash
docker compose run --rm --user "$(id -u):$(id -g)" web python manage.py <command>
```

Example:

```bash
docker compose run --rm --user "$(id -u):$(id -g)" web python manage.py startapp another_app
```

---

## Troubleshooting

### Docker daemon error on macOS

If you see an error like:

```text
failed to connect to the docker API at unix:///Users/.../docker.sock
```

Start Docker Desktop, then run the command again:

```bash
docker compose up -d
```

### Database container is unhealthy

Check database logs:

```bash
docker compose logs -f db
```

If this is a fresh development setup and you do not need the old database data, reset the database volume:

```bash
docker compose down -v
```

```bash
docker compose build --no-cache db
```

```bash
docker compose up -d
```

Then run migrations again:

```bash
docker compose exec web python manage.py migrate
```

### Missing `.env` values

If Django fails during startup, confirm that `.env` contains:

```env
DJANGO_SECRET_KEY=change-this-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
POSTGRES_DB=property_db
POSTGRES_USER=property_user
POSTGRES_PASSWORD=property_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### First embedding command is slow or fails

The project uses `sentence-transformers`. On first use, the model must be downloaded inside the container.

Make sure the container has internet access, then run:

```bash
docker compose exec web python manage.py generate_embeddings
```

### Imported properties do not change after editing CSV

The import command uses `get_or_create`. If a property with the same generated slug already exists, it will not update that existing row.

For local testing, either:

- delete the existing property from Django Admin, then import again
- reset the database with `docker compose down -v`
- update the import command to use `update_or_create` instead of `get_or_create`

---

## Development Notes

- Keep templates modular by using files inside `property_app/templates/property_app/partials/`.
- Keep static CSS and JavaScript inside `property_app/static/property_app/`.
- Use `select_related("location")` when listing properties to avoid unnecessary database queries.
- Use PostGIS `Distance` annotation when showing distance from property to city/location.
- Use `pgvector` for semantic fallback location search.

---

## Assignment Coverage

This project covers the main assignment requirements:

- Import vacation rental properties from CSV
- Store property images
- Show properties and locations in Django Admin
- Add admin filters and search fields
- Implement homepage with search form
- Implement location autocomplete API
- Search properties by location
- Show search results in property listing page
- Add pagination to property listing page
- Create property detail page
- Show images and amenities on detail page
- Show distance from city/location on detail page

---

## License

This project is for educational and assignment purposes.