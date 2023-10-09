**Cached scoring-api**

It uses tarantool as a key-value cache.


To build dokcer containers:

    docker-compose build

To start containers;

    docker-compose up

Tests

If your docker compose version is 2.x then:
    
    bash test.sh

If your docker compose version is 1.x then:
    
    bash test-dock-comp-v1.sh