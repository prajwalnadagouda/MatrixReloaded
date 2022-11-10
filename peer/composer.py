import yaml
from random import randint, randrange
import sys

p1=randint(10000, 65536)
p2=randint(10000, 65536)
# p3=randint(10000, 65536)

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0

config = ConfigParser()
config.add_section('ports')
config.set('ports', '5000', str(p1))
config.set('ports', '2006', str(p2))
# config.set('ports', '2007', str(p3))
config.add_section('host')
config.set('host', 'id', str(sys.argv[1]))

with open('info.ini', 'w') as configfile:
    config.write(configfile)

names_yaml = """
version: '2.2'
services:
    app:
        build: ./app
        # links:
        #     - db
        ports:
            - "{}:5000"
            - "{}:2008"
            #- "{}:2007"
        networks:
            - peercmpe273
        volumes:
            - ./info.ini:/app/info.ini

networks:
    peercmpe273:
        driver: bridge
        ipam:
            driver: default
            config:
                - subnet: 172.59.0.0/16
"""
names_yaml=names_yaml.format(p1,p2)#,p3)
names = yaml.safe_load(names_yaml)
with open('docker-compose.yml', 'w') as file:
    yaml.dump(names, file)


