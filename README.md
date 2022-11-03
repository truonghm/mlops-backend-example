# Back-end Demo for Quantity Prediction Model (Pod Foods)


## Setting up

### Prerequisites

You will need:

1. python (3.8): install with [miniconda](https://docs.conda.io/en/main/miniconda.html) or [the official release](https://www.python.org/downloads/release/python-380/)
2. [docker](https://docs.docker.com/engine/install/) and [docker-compose](https://docs.docker.com/compose/install/)

### Installation

1. Clone this repository:
```
git clone git@github.com:truonghm/pf-backend.git
cd pf-backend
```

2. Create a new Python environment for isolation. If you use `conda`, you can use the following commands:

```
conda create --name pf python=3.8
conda activate pf
```

3. Next, install the neccessary packages:
```
pip install -r requirements.txt
```

4. Create the environment variable file: Simply rename the `.env.example` file to `.env`. 

## Usage


1. To start the serivces, run:

```bash
docker-compose up
```

2. Copy the raw data (3 csv files, `data_metadata_product.csv`, `data_metadata_store.csv`, `data_order.csv` into the `training/data` folder). I do not upload these files to Github as they are (supposely) confidential.

3. To prepare data and train model, run:

```bash
cd training
python preprocess.py && python train.py
```

4. Access the services with:
    - API docs: [localhost:8000/documentation](localhost:8000/documentation)
    - MLFlow: [localhost:5000](localhost:5000)
    - Prometheus: [localhost:9090](localhost:9090)
    - Grafana: [localhost:3000](localhost:3000)
    - Airflow: TBU

### System architecture

[Insert picture here]

### API documentation

#### Endpoint URL

> http://127.0.0.1:8000/quantity/predict

#### API information

| API info        | Detail |
| --------------- | ------ |
| Response format | JSON   |
| Authentication  | No     |
| Method          | POST   |

#### Parameters

#### Example Requests

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/quantity/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "input": [
    {
      "store_id": 55,
      "product_id": 1866
    },
    {
      "store_id": 55,
      "product_id": 1867
    },
    {
      "store_id": 55,
      "product_id": 1939
    }
  ],
  "date": "string"
}'
```

#### Example Response

```
{
  "predictions": [
    2,
    3
  ]
}

```


### Model development

### Model registry

MLflow
```
mlflow server --backend-store-uri=sqlite:///artifacts.db --default-artifact-root=file:training/mlruns --host 0.0.0.0 --port 5000
```

Feast

### ETL

Database


Airflow
```

```

### Monitoring


### Testing


## Task list

- [x] Build skeleton (FastAPI + Grafana + Prometheus)  
- [x] Dockerize  
- [x] Add MLflow  
- [x] Add MySQL  
- [ ] Add Airflow  
- [ ] Add quality-of-life features:    
    - [ ] Automatically add datasource and dashboard for Grafana at build  
    - [ ] Feature store (Feast)  
    - [x] Simulation for API endpoint (Locust)  
    - [ ] Unit testing  
    - [ ] Improve `.env`  
- [ ] Write documentation  
    - [ ] Set-up and how-to-use  
	- [ ] Doc for API endpoint  
    - [ ] System architecture  