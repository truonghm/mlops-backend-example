FROM apache/airflow:2.4.2-python3.8

COPY requirements.txt /requirements.txt
RUN pip install --user --upgrade pip
RUN pip install --no-cache-dir --user -r /requirements.txt

WORKDIR /opt/airflow
ENV PYTHONPATH="${PYTHONPATH}:/opt/airflow/dags/repo"
