# Property Management System

Django property management project backed by PostgreSQL 18 with PostGIS and pgvector.

## Docker Setup

The Docker setup builds native images on both x86 Linux and Apple Silicon Macs. Do not set a fixed Docker `platform` unless you explicitly want emulation.

### Prerequisites

- Docker Desktop on macOS, or Docker Engine with the Compose plugin on Linux
- Git

### Configure Environment

Create a local `.env` file from the example:

```sh
cp .env.example .env
```

Edit `.env` and set real values for at least:

```sh
POSTGRES_DB=propertydb
POSTGRES_USER=postgres
POSTGRES_PASSWORD=change_me_to_a_strong_password
DJANGO_SECRET_KEY=change_me_to_a_random_50_char_string
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

On Linux, set your host UID/GID so files created from inside the web container are owned by your user:

```sh
echo "HOST_UID=$(id -u)" >> .env
echo "HOST_GID=$(id -g)" >> .env
```

On macOS this is usually optional, but it is safe to set.

### Build Images

Build both services:

```sh
docker compose build
```

This builds:

- `web`: Python 3.13 Django image
- `db`: PostgreSQL 18 image with PostGIS installed and pgvector compiled for the current CPU architecture

To rebuild without cache:

```sh
docker compose build --no-cache
```

To use a different pgvector tag:

```sh
PGVECTOR_VERSION=v0.8.3 docker compose build db
```

### Run Services

Start the stack:

```sh
docker compose up -d
```

Open the app at:

```text
http://localhost:8000/
```

PostgreSQL is exposed on host port `5442` and container port `5432`.

### Run Migrations

After the services are healthy, run migrations:

```sh
docker compose exec web python manage.py migrate
```

Create an admin user if needed:

```sh
docker compose exec web python manage.py createsuperuser
```

### Useful Commands

View service status:

```sh
docker compose ps
```

View logs:

```sh
docker compose logs -f
```

Stop services:

```sh
docker compose down
```

Stop services and remove the database volume:

```sh
docker compose down -v
```

## Author

**Rangon Roy Utsab**

