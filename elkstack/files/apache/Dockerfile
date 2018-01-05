FROM httpd:2.4
ENV REGION eu-west-1
COPY /var/lib/go-agent/pipelines/elkstack/elkstack/files/apache/public_html/ /usr/local/apache2/htdocs/
COPY /var/lib/go-agent/pipelines/elkstack/elkstack/files/apache/httpd.conf /usr/local/apache2/conf/httpd.conf
