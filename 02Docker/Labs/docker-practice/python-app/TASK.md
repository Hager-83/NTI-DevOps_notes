# Exercise 1 — Dockerize a Python (Flask) App

## What's here
A small Flask web app (`app.py`) with two routes:
- `GET /` — returns a JSON greeting
- `GET /health` — returns a JSON health check

There is **no Dockerfile** in this folder. That's your job.

## Your tasks
1. Write a `Dockerfile` that:
   - Uses an official, slim Python base image (pick an appropriate tag/version).
   - Copies `requirements.txt` first and installs dependencies **before** copying the rest of the app code (think about why the order matters for build caching).
   - Copies the application code into the image.
   - Exposes the port the app listens on.
   - Runs the app with `CMD` (not by opening a shell manually).
2. Build the image:
   ```
   docker build -t python-app .
   ```
3. Run a container from it, mapping host port `8000` to the container's port:
   ```
   docker run -p 8000:5000 python-app
   ```
4. Confirm it works by visiting `http://localhost:8000/` and `http://localhost:8000/health`.
5. Run `docker image ls` and note the image size. Try to make the image smaller (e.g. `python:3.12-slim` instead of the full `python:3.12`, or add a `.dockerignore`). Record the before/after size.

## Stretch goals
- Add a `.dockerignore` file (what should NOT be copied into the image?).
- Set the `PORT` environment variable using `-e PORT=8080` when running the container and confirm the app picks it up.
- Run the container in detached mode (`-d`), then use `docker logs` and `docker exec -it <container> sh` to inspect it.
- Add a `HEALTHCHECK` instruction to the Dockerfile that curls `/health`.

## Questions to answer in your submission
1. What base image did you choose, and why?
2. What is the final image size, and what did you do (if anything) to reduce it?
3. What does `EXPOSE` actually do — does it publish the port by itself? Explain.
4. What's the difference between `CMD` and `ENTRYPOINT`? Which did you use and why?
