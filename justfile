build:
    docker build --rm -t python-pipeline:$(git rev-parse HEAD) -t python-pipeline:latest .

build-linux:
    docker buildx build --platform linux/amd64 -t python-pipeline:$(git rev-parse HEAD) -t python-pipeline:latest .

run:
    poetry run python main.py
