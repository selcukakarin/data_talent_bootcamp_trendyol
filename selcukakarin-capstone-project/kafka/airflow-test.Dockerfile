FROM python:3.7

LABEL maintainer="OnurTashan"
LABEL name="OT_Airflow_"
LABEL version="1_0"

# Never prompt the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND noninteractive
ENV TERM linux


ARG AIRFLOW_USER_HOME=/usr/local/airflow

ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}
#ENV PYTHONPATH="/usr/local/airflow/dags"
COPY ./requirements ${AIRFLOW_USER_HOME}/

RUN set -ex \
    && buildDeps=' \
        freetds-dev \
        libkrb5-dev \
        libsasl2-dev \
        libssl-dev \
        libffi-dev \
        libpq-dev \
        git \
    ' \
    && useradd -ms /bin/bash -d ${AIRFLOW_USER_HOME} airflow \
    && apt-get update -yqq \
    && apt-get upgrade -yqq \
    && apt-get install -yqq --no-install-recommends \
        $buildDeps \
        freetds-bin \
        build-essential \
        default-libmysqlclient-dev \
        apt-utils \
        curl \
        rsync \
        netcat \
        locales \
        python3-dev \
        libpq-dev \
    && locale-gen \
    && apt-get purge --auto-remove -yqq $buildDeps \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && pip install apache-airflow==2.0.0 \
    && pip install psycopg2-binary \
    && pip install -r ${AIRFLOW_USER_HOME}/requirements.txt

COPY ./conf/airflow.cfg ${AIRFLOW_USER_HOME}/airflow.cfg


#RUN pip3 install -r ${PIP_REQUIREMENTS}/requirements.txt

ENV TZ=Europe/Istanbul
RUN unlink /etc/timezone
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN chown -R airflow: ${AIRFLOW_USER_HOME}

EXPOSE 8080 8793

USER airflow
WORKDIR ${AIRFLOW_USER_HOME}