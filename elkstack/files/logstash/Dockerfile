FROM docker.elastic.co/logstash/logstash-oss:6.2.4

MAINTAINER John Hudson version: 0.1

RUN curl -O https://bootstrap.pypa.io/get-pip.py
RUN python get-pip.py --user
RUN /usr/share/logstash/.local/bin/pip install credstash --user
RUN rm -f /usr/share/logstash/pipeline/logstash.conf
RUN /usr/share/logstash/bin/logstash-plugin install logstash-input-sqs && \
/usr/share/logstash/bin/logstash-plugin install logstash-codec-cloudwatch_logs && /usr/share/logstash/bin/logstash-plugin install logstash-filter-cipher && /usr/share/logstash/bin/logstash-plugin install logstash-input-kinesis && /usr/share/logstash/bin/logstash-plugin install logstash-filter-json &&  /usr/share/logstash/bin/logstash-plugin install logstash-input-gelf && /usr/share/logstash/bin/logstash-plugin install logstash-input-cloudwatch && /usr/share/logstash/bin/logstash-plugin install logstash-input-s3 && /usr/share/logstash/bin/logstash-plugin install logstash-input-cloudwatch_logs
ADD cloudflare_log_get.py /usr/share/logstash/
ADD pipeline/ /usr/share/logstash/pipeline/
ADD config/ /usr/share/logstash/config/
ENV AWS_DEFAULT_REGION eu-west-1
