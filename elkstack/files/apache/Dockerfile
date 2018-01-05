FROM ubuntu:16.04
ENV REGION eu-west-1
RUN apt update
RUN apt install -y apache2
RUN echo "Welcome to my web site" > /var/www/html/index.html
EXPOSE 443
CMD ["/usr/sbin/apache2", "-D", "FOREGROUND"]
