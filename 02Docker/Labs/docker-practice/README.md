# Docker Practical Exercises

A set of five hands-on Docker exercises for students, covering Dockerfiles across several languages plus
Docker Compose. Each exercise folder is self-contained and has its own `TASK.md` with step-by-step instructions
and questions to answer.

## Structure

| Folder               | Language / Stack        | Focus                                              |
|-----------------------|--------------------------|-----------------------------------------------------|
| `python-app/`         | Python (Flask)           | Basic Dockerfile, layer caching, image size         |
| `nodejs-app/`         | Node.js (Express)        | Layer caching, multi-stage builds, non-root user    |
| `java-app/`           | Java (JDK HttpServer)    | Multi-stage builds, JDK vs JRE image size            |
| `go-app/`             | Go (standard library)    | Multi-stage builds, `scratch` images, static binaries |
| `compose-exercise/`   | Python (Flask) + Redis   | Docker Compose, multi-container networking, volumes  |

## Suggested order

1. `python-app/` — the gentlest introduction (single-stage Dockerfile).
2. `nodejs-app/` — same idea, then push into multi-stage builds and non-root users.
3. `java-app/` — multi-stage builds become almost necessary because JDK images are large.
4. `go-app/` — the payoff: a multi-stage build down to a few-megabyte (or `scratch`) image.
5. `compose-exercise/` — bring two containers up together and network them with Compose.

## What students turn in

For each exercise:
- The `Dockerfile` (and `docker-compose.yml` for exercise 5) they wrote.
- A screenshot or terminal output showing the container running and the endpoints responding.
- Written answers to the questions listed at the bottom of that exercise's `TASK.md`.

## Requirements

Students need Docker Desktop (or Docker Engine + Compose plugin) installed locally. No language runtimes need to
be installed on the host — that's the point of the exercise.

## Instructor notes

- None of the folders include a `Dockerfile` on purpose — writing it is the assignment.
- Difficulty increases gradually: exercise 1 is a straightforward single-stage build, and by exercise 4 students are
  writing multi-stage builds targeting `scratch`.
- Exercise 5 is the only one that requires Compose and is a natural capstone — it also revisits volumes and
  environment variables from the Dockerfile exercises.
- Suggested pairing: assign the theoretical question set (PDF) alongside exercises 1–2, then have students revisit
  the multi-stage / networking questions in the PDF after finishing exercises 3–5.
