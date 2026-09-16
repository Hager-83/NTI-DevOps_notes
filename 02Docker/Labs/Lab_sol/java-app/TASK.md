# Exercise 3 — Dockerize a Java App

## What's here
A single-file Java app (`Main.java`) using only the JDK's built-in `HttpServer` — no build tool or external
dependencies required. Routes:
- `GET /` — JSON greeting
- `GET /health` — health check

There is **no Dockerfile** here. That's your job.

## Your tasks
1. Write a `Dockerfile` that compiles and runs the app. Two common approaches — pick one:
   - **Single-stage**: use a JDK image, `COPY Main.java .`, run `javac Main.java` in a `RUN` step, then `CMD ["java", "Main"]`.
   - **Multi-stage (recommended, try this one)**: compile in a `FROM eclipse-temurin:21-jdk AS build` stage, then copy only the compiled
     `.class` file(s) into a smaller `FROM eclipse-temurin:21-jre` runtime stage.
2. Build and run:
   ```
   docker build -t java-app .
   docker run -p 8000:8080 java-app
   ```
3. Verify `http://localhost:8000/` and `http://localhost:8000/health`.

## Stretch goals
- Compare the image size of the single-stage vs. multi-stage version. Java build images (JDK) are large — how much
  smaller is the runtime-only (JRE) image?
- Pass the port via `-e PORT=9090` and confirm the app respects it.
- Look up why running Java in containers used to have memory issues (JVM not respecting container memory limits) and
  what changed in modern JDKs.

## Questions to answer in your submission
1. What is the difference between a JDK image and a JRE image? Which does your final runtime stage use?
2. How much smaller is your multi-stage image compared to a naive single-stage build? Show `docker image ls` output.
3. In a multi-stage build, what happens to the `build` stage after the final image is produced — is it kept anywhere?
4. Why might you *not* want a compiler (`javac`) present in your production image at all?
