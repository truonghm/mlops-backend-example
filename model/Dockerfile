FROM python:3.8

WORKDIR /pf/

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "model/run_app.py" ]