# First stage: Build the Go application
FROM golang:1.24 AS build

WORKDIR /app

COPY go.mod ./

COPY main.go ./

ENV CGO_ENABLED=0

RUN go build -o app .

# Second stage: Create a lightweight image for running the application
FROM scratch

COPY --from=build /app/app .

EXPOSE 8080

CMD ["./app"]