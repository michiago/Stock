
set -e

docker build -t stock ./docker/
docker run -it --rm -w /app -v $(pwd)/:/app stock /bin/bash