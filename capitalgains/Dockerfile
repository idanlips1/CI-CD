FROM openjdk:17-jdk-slim

WORKDIR /app

COPY target/capitalgains-0.0.1-SNAPSHOT.jar capital-gains.jar

EXPOSE 8080

ENV STOCKS1_URL=http://stocks1:8000


CMD ["java", "-jar", "capital-gains.jar"] 