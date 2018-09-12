FROM docker.elastic.co/elasticsearch/elasticsearch:6.4.0
ENV REGION eu-west-1
ADD elasticsearch.yml /usr/share/elasticsearch/config/
USER root
RUN chown elasticsearch:elasticsearch config/elasticsearch.yml
USER elasticsearch
WORKDIR /usr/share/elasticsearch
RUN bin/elasticsearch-plugin install --batch discovery-ec2 && bin/elasticsearch-plugin install --batch repository-s3  && sed -e '/^-Xm/s/^/#/g' -i /usr/share/elasticsearch/config/jvm.options

#/usr/share/elasticsearch/bin/elasticsearch-plugin install --batch discovery-ec2
