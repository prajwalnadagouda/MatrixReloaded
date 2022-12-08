#!/bin/bash
python3 composer.py $1
docker-compose up --build
