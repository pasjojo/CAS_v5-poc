FROM docker.io/php:5.6-apache
ENV APACHE_LOCK_DIR=/tmp
ENV APACHE_RUN_USER=www-data
ENV APACHE_RUN_GROUP=www-data
ENV APACHE_LOG_DIR=/var/log/apache2/
ENV APACHE_PID_FILE=/tmp/apache2.pid
RUN apt-get update && apt-get install -y git automake build-essential libtool apache2-dev libcurl4-openssl-dev libssl-dev && apt-get clean all

WORKDIR /tmp
RUN git clone https://github.com/apereo/mod_auth_cas \
    && cd /tmp/mod_auth_cas \
    && autoreconf -ivf \
    && ./configure \
    && make \
    && cp ./src/.libs/mod_auth_cas.so /usr/lib/apache2/modules/
COPY auth_cas.load /etc/apache2/mods-available/auth_cas.load
RUN ln -s /etc/apache2/mods-available/auth_cas.load /etc/apache2/mods-enabled/auth_cas.load 

RUN apt-get remove -y automake build-essential libtool apache2-dev libcurl4-openssl-dev libssl-dev \
    && apt-get autoremove -y

RUN mkdir -p /usr/share/ca-certificates/cas && mkdir -p /var/cache/apache2/mod_auth_cas/ 
COPY apca_test_cas.crt /usr/share/ca-certificates/cas
COPY auth_cas.conf /etc/apache2/mods-available/auth_cas.conf
RUN ln -s /etc/apache2/mods-available/auth_cas.conf /etc/apache2/mods-enabled/auth_cas.conf
COPY cas.conf /etc/apache2/sites-available/cas.conf
RUN ln -s /etc/apache2/sites-available/cas.conf /etc/apache2/sites-enabled/ && rm -f /etc/apache2/sites-enabled/000*
COPY html/ /var/www/html/

