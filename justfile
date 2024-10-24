build-docker:
    docker build -t python-pipeline:$(git rev-parse HEAD) .
