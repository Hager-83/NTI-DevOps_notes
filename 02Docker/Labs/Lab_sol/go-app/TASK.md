# Exercise 4 — Dockerize a Go App

## What's here
A tiny Go HTTP server (`main.go`, `go.mod`) using only the standard library. Routes:
- `GET /` — JSON greeting
- `GET /health` — health check

There is **no Dockerfile** here. That's your job — and this one is the best candidate for showing off a truly tiny
final image.

## Your tasks
1. Write a **multi-stage** Dockerfile:
   - Stage 1 (`build`): use a `golang` base image, copy the source, run `go build -o app .` to produce a static binary.
   - Stage 2 (final): copy **only the compiled binary** into a minimal base image (try `scratch` or `alpine`) and run it.
2. Build and run:
   ```
   docker build -t go-app .
   docker run -p 8000:8080 go-app
   ```
3. Verify `http://localhost:8000/` and `http://localhost:8000/health`.

## Stretch goals
- Try building the final stage `FROM scratch`. If it fails or behaves oddly, figure out why (hint: CGO, or missing
  CA certificates/timezone data) and either fix it or fall back to `alpine` and explain the trade-off.
- Compare the final image size against every other exercise in this set. Go should win by a wide margin — why?
- Add build flags to strip debug symbols (`-ldflags="-s -w"`) and measure the size difference.

## Questions to answer in your submission
1. What is `scratch`, and why can Go (but not Python or Node) realistically run on top of it?
2. What is the final image size? Rank all four language exercises (Python, Node, Java, Go) by image size and explain
   the pattern you see.
3. What does `CGO_ENABLED=0` do when building the Go binary, and why does it matter for a `scratch`-based image?
