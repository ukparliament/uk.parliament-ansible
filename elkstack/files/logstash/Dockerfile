# A basic apache server. To use either add or bind mount content under /var/www
FROM docker.elastic.co/logstash/logstash:5.6.5

MAINTAINER John Hudson version: 0.1

ADD logstash.yml /usr/share/logstash/config/logstash.yml

EXPOSE 5061
