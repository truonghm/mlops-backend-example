FROM python:3.8

WORKDIR /simulation/

COPY . .
RUN pip install -r requirements.txt 

EXPOSE 8089
CMD ["locust", "-f", "locust_test.py", "--host", "http://app:8000"]