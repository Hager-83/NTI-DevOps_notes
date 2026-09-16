# Exercise 5 — Docker Compose: Multi-Container App

## What's here
A Flask app (`app.py`) that connects to Redis to keep a visit counter.
- `GET /` — increments a counter in Redis and returns the current count
- `GET /health` — reports whether the app and Redis connection are healthy

The app reads its Redis connection info from environment variables: `REDIS_HOST` (default `localhost`) and
`REDIS_PORT` (default `6379`).

There is **no Dockerfile** and **no docker-compose.yml** here. Both are your job.

## Your tasks
1. Write a `Dockerfile` for the Flask app (same idea as Exercise 1).
2. Write a `docker-compose.yml` in this folder that defines **two services**:
   - `web` — built from your Dockerfile, publishes port `8000` on the host, mapped to the app's port.
   - `redis` — uses the official `redis:7-alpine` image (no Dockerfile needed, just pull it).
3. Make sure the `web` service can reach Redis by its **service name** as the hostname (that's what Compose's
   built-in networking gives you for free — set `REDIS_HOST=redis` as an environment variable on the `web` service).
4. Bring everything up:
   ```
   docker compose up --build
   ```
5. Visit `http://localhost:8000/` a few times and confirm the counter increases. Visit `/health` and confirm Redis
   shows as healthy.
6. Stop everything with `docker compose down`. Then bring it back up — does the counter reset? Why or why not?

## Stretch goals
- Add a **named volume** for Redis so data survives `docker compose down` (but not `docker compose down -v`).
- Add a `depends_on` with a `condition: service_healthy` so `web` waits for Redis to actually be ready, not just
  started (you'll need a `healthcheck:` block on the `redis` service).
- Scale the web service: `docker compose up --scale web=3` — what happens to the port mapping, and why?
- Split configuration into `docker-compose.yml` + `docker-compose.override.yml` for local dev vs. a
  `docker-compose.prod.yml` for a leaner production setup.

## Questions to answer in your submission
1. How did `web` find `redis` on the network without you specifying an IP address? Explain Compose's default
   networking behavior.
2. What is the difference between `docker compose down` and `docker compose down -v`? Which one did you use, and
   what happened to your counter each time?
3. What does `depends_on` guarantee by default — does it wait for the dependency to be *ready*, or just *started*?
   How did you address that (if you did the stretch goal)?
4. If you wanted to run three copies of the `web` service behind a load balancer, what would you need to change
   about the port mapping?
