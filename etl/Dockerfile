FROM apache/airflow:2.1.2-python3.8

USER root

COPY requirements.txt /requirements.txt
RUN pip3 install --no-cache-dir --use-deprecated=legacy-resolver -r /requirements.txt

WORKDIR /opt/airflow
ENV PYTHONPATH="${PYTHONPATH}:/opt/airflow/dags/repo"
