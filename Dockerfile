FROM centos:centos6
MAINTAINER Giuseppe Paterno' <gpaterno@gpaterno.com>

LABEL Description="SecurePass Self-Service Portal"

## Updates
RUN yum -y update

## Install EPEL stuffs
RUN rpm -ihv http://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm

## Install pre/coreq
RUN yum -y install httpd mod_wsgi python-pip python-virtualenv gcc zlib-devel libjpeg-turbo-devel MySQL-python supervisor uwsgi-plugin-python

## Cleanup
RUN yum -y clean all

## Copy SecurePass
RUN mkdir -p /srv/securepass-self
COPY . /srv/securepass-self

## Install pip requisites
RUN virtualenv --system-site-packages /srv/securepass-self ; source /srv/securepass-self/bin/activate ; cd /srv/securepass-self ; pip install -r requirements.txt

## Copy apache conf
#COPY extras/dreamliner.conf /etc/httpd/conf.d/dreamliner.conf
#COPY extras/supervisord.conf /etc/supervisord.conf 

EXPOSE 80

WORKDIR /srv/securepass-core
CMD /bin/bash
#CMD /usr/bin/supervisord
