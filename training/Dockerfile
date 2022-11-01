FROM python:3.7-slim-buster

WORKDIR /mlflow/
RUN pip install mlflow boto3

EXPOSE 5000

ENV BACKEND_URI sqlite:///artifacts.db
ENV ARTIFACT_ROOT /mlflow/artifacts

CMD mlflow server --backend-store-uri ${BACKEND_URI} --default-artifact-root ${ARTIFACT_ROOT} --host 0.0.0.0 --port 5000