#!/usr/bin/env bash

set -e

docker pull mariadb
docker pull postgres
docker pull neo4j

docker run --name mariadb -e MYSQL_ROOT_PASSWORD=123 -p 3306:3306 -d mariadb
docker run --name postgres -e POSTGRES_PASSWORD=123 -d -p 5432:5432 postgres
docker run --name neo4j -p7474:7474 -p7687:7687 -d --env NEO4J_AUTH=neo4j/123 neo4j
