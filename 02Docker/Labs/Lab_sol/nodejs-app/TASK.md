# Exercise 2 — Dockerize a Node.js (Express) App

## What's here
A small Express app (`index.js`) with:
- `GET /` — JSON greeting
- `GET /health` — health check

There is **no Dockerfile**, `package-lock.json`, and no `node_modules` here yet. That's part of the task.

## Your tasks
1. Write a `Dockerfile` that:
   - Uses an official Node LTS image (choose an appropriate/slim tag).
   - Copies `package.json` (and lockfile, once you generate one) and runs `npm install` **before** copying the rest of the source — this is a caching-layer exercise, same idea as exercise 1 but in Node.
   - Copies the app source.
   - Exposes the port the app listens on.
   - Starts the app with `CMD ["node", "index.js"]` (or `npm start`).
2. Build and run:
   ```
   docker build -t node-app .
   docker run -p 8000:3000 node-app
   ```
3. Verify `http://localhost:8000/` and `http://localhost:8000/health`.

## Stretch goals
- Use a **multi-stage build**: one stage to install dependencies, a final smaller stage that only copies `node_modules` + source into a lean runtime image.
- Run the container as a **non-root user** (research the `USER` instruction).
- Add a `.dockerignore` that excludes `node_modules` and any local `.env` files.
- Set `NODE_ENV=production` as an environment variable in the Dockerfile and explain what it changes.

## Questions to answer in your submission
1. Why do we copy `package.json` before the rest of the source code?
2. What is a multi-stage build, and did you use one? What problem does it solve?
3. Why is running a container as a non-root user considered a security best practice?
4. Compare your final Node image size to the Python image size from Exercise 1. Are they comparable? Why or why not?
