
## Reddit-API-data-pipeline

## Objective:
Create a batch data pipeline to ingest Reddit data from its API (for any chosen sub-reddit). The end goal is build a dashboard/report, providing insight into the user engagement metrics of the selected subreddits.


### Architecture/Flow:
<!-- ![Reddit Data Ingestion Pipeline (Batch)](./static/reddit-data-pipeline-flow.png "Reddit Data Ingestion Pipeline (Batch)") -->
<img src="./static/reddit-data-pipeline-flow.png" width=79% height=79%>


### Setup/Instructions:
#### 1. Pre-requisites
- GCP Account & Terraform (Cloud Storage & Biq Query will be used).
- Make sure Docker is installed & Logged in to the Docker CLI using `docker login`.
- Reddit API requires Auth, login & create an [app](https://www.reddit.com/prefs/apps) to get credentials (skip this step, as already migrated the pipeline to use pushshift API).
- Signup for a free ![dbt cloud](https://cloud.getdbt.com/) developer account & connect with github to read/write to this git repo.


#### 2. Clone the repo to get started
- Create a Virtual environemnt & Activate it.
    ```shell
    # create env
    python -m venv <env-name>
    
    # activate env
    source <env-name>/bin/activate
    ```


- Install requirements using `requirements.txt` file.
    ```shell
    pip3 install -r requirements.txt
    ```

- Clone this repo & Change the directory.
    ```shell
    git clone https://github.com/Asrst/reddit-api-data-pipeline.git

    cd reddit-api-data-pipeline
    ```


#### 3. Setup gcp infra setup using terraform
- Setup gcp project, enable api's and download the credentials json - refer this ![`gcp_setup.md`](./terraform/gcp_setup.md).
- Navigate to terraform directory & refer the folder ![`terraform`](./terraform/README.md) for commands to run.
    ```shell
    cd terraform
    ```
#### 4. Extract and load data into gcs & big query external tables
**Ideal Option: Using Airflow as Orchestrator**
- Navigate to `airflow` directory & Create two new directories for airflow logs & plugins.
    ```shell
    cd airflow

    mkdir logs plugins
    ```
- Setup Airflow using docker & docker-compose. Refer ![`airflow`](./airflow/) for detailed steps.
- Refer the dags in `airflow/dags` which contains code for quering api & loading data into gcs/big-query.
- The pipeline DAG is scheduled to run on monthly basis. Trigger it manually to test run it.

**Alternate Option: As the data is small, use python scripts to extract & load the data using python scripts**
- To extract and store the data to GCS & create big query external tables, run the scripts in `scripts/` folder.
- Run the commands for different subreddit for which data needs to be collected (gcs bucket & bq dataset will remain same).

    ```shell
    # next 2 commands assumes you are in airflow folder, if not run cd command.
    cd airflow
    # extracts data from api & store to gcs
    python3 ../scripts/test_pushshift.py --gcs_bucket="dl-reddit-api-404" --sub_reddit="ipl" --year=2022
    # creates a big query external table
    python3 ../scripts/test_bq_load.py --bq_dataset="reddit_api" --table_name="ext_ipl" --gcs_uri="gs://dl-reddit-api-404/ipl/posts-2022-*.csv"
    ```


#### 5. Transform data in big query using dbt
- Fork this repo into your git account & Login into your dbt cloud account.
- Setup new project by providing link your newly forked git repo & gcp creditional json (if not already done).
- Transform data using dbt & Create a data mart. Refer ![`dbt`](./dbt/) for detailed steps.
- Schedule the runs on monthly basis to update the datamarts regularly (as airflow pipeline also runs monthly)

*Alternatively you can run the dbt commands in the local, but wont be able to scheduled runs without an Orchestrator*

#### 6. Visualise the data & create the reports
- Create a account at preset.io & add big query as new data source by providing gcp creditional json.
- Create datasets from newly created data mart to visualise/report or create dashboards.

**Important Note:** 
- preset.io (or superset) doesnt allow public dashboard sharing outside of workspace (users needs to be in same workspace for sharing to work). hence [this dashboard](https://26fa4707.us1a.app.preset.io/superset/dashboard/8/?native_filters_key=px_ojJllrgVakoPASbKWOGpJ7-GnsJxS4Qs4zCrfp89gwTq0anpz7nnuBlCKujI3) is not publicly availble .


### Result/Output:
<img src="./static/superset-preset-reddit-analytics.jpg" width=79% height=79%>


<br>

**References to tools & technologies used:**: 
- Programming Language - [**Python**](https://www.python.org)
- Infrastructure as Code software - [**Terraform**](https://www.terraform.io)
- Containerization - [**Docker**](https://www.docker.com), [**Docker Compose**](https://docs.docker.com/compose/)
- Orchestration - [**Airflow**](https://airflow.apache.org)
- Transformation - [**dbt**](https://www.getdbt.com)
- Data Lake - [**Google Cloud Storage**](https://cloud.google.com/storage)
- Data Warehouse - [**BigQuery**](https://cloud.google.com/bigquery)
- Data Visualization - [**Preset.io**](https://preset.io/)

