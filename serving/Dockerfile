FROM python:3.8

WORKDIR /pf/

COPY . .

RUN pip install --user --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "main.py" ]