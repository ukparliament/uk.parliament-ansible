# A basic apache server. To use either add or bind mount content under /var/www
FROM docker.elastic.co/logstash/logstash:6.2.1

MAINTAINER John Hudson version: 0.1

RUN yum -y install python-pip
RUN pip install credstash
RUN rm -f /usr/share/logstash/pipeline/logstash.conf
RUN /usr/share/logstash/bin/logstash-plugin install logstash-input-sqs && \
 /usr/share/logstash/bin/logstash-plugin install logstash-filter-json &&  /usr/share/logstash/bin/logstash-plugin install logstash-input-gelf && /usr/share/logstash/bin/logstash-plugin install logstash-input-cloudwatch
ADD cloudflare_log_get.py /usr/share/logstash/
ADD pipeline/ /usr/share/logstash/pipeline/
ADD config/ /usr/share/logstash/config/
