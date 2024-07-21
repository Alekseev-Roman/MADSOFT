FROM postgres:alpine

ADD ./sql_db_initialization.sql /docker-entrypoint-initdb.d

RUN chmod a+r /docker-entrypoint-initdb.d/*
