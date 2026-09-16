# First stage: Build the Java application
FROM eclipse-temurin:21-jdk AS build

WORKDIR /app

COPY Main.java .

RUN javac Main.java


# Second stage: Create a lightweight image for running the application
FROM eclipse-temurin:21-jre

WORKDIR /app

COPY --from=build /app/Main.class .

EXPOSE 8080

CMD ["java", "Main"]