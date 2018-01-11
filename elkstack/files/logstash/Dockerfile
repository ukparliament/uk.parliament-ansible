# A basic apache server. To use either add or bind mount content under /var/www
FROM docker.elastic.co/logstash/logstash:5.6.5

MAINTAINER John Hudson version: 0.1

ADD logstash.yml /usr/share/logstash/config/logstash.yml
ADD logstash.conf /usr/share/logstash/pipeline/logstash.conf

EXPOSE 5061 8000

RUN logstash-plugin install logstash-filter-truncate
RUN logstash-plugin install logstash-filter-geoip
RUN logstash-plugin install logstash-filter-cidr
RUN logstash-plugin install logstash-http-input
