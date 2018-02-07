# A basic apache server. To use either add or bind mount content under /var/www
FROM docker.elastic.co/logstash/logstash-oss:6.1.3

MAINTAINER John Hudson version: 0.1

RUN rm -f /usr/share/logstash/pipeline/logstash.conf
RUN /usr/share/logstash/bin/logstash-plugin install logstash-input-sqs && \
 /usr/share/logstash/bin/logstash-plugin install logstash-filter-json &&  /usr/share/logstash/bin/logstash-plugin install logstash-input-gelf
ADD pipeline/ /usr/share/logstash/pipeline/
ADD config/ /usr/share/logstash/config/
