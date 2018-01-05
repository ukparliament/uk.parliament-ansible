FROM httpd:2.4
ENV REGION eu-west-1
COPY apache/public_html/ /usr/local/apache2/htdocs/
COPY httpd.conf /usr/local/apache2/conf/httpd.conf
CMD /usr/sbin/apache2ctl -D FOREGROUND
