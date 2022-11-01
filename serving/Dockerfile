FROM python:3.8

WORKDIR /pf/

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "serving/main.py" ]