#! /usr/bin/env sh

# This starts tests with docker-compose version 1.+

# Exit in case of error
set -e

docker-compose \
-f docker-compose.yml \
config > docker-stack.yml

docker-compose -f docker-stack.yml build
docker-compose -f docker-stack.yml down -v --remove-orphans # Remove possibly previous broken stacks left hanging after an error
docker-compose -f docker-stack.yml up -d
docker exec -it cached-score-api-app-1 bash /code/tests/test-start.sh "$@"
docker-compose -f docker-stack.yml down -v --remove-orphans