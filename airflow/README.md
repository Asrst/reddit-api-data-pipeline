### Airflow Setup.

To orchestrate this, we'll use [Apache Airflow](https://airflow.apache.org/docs/apache-airflow/stable/tutorial.html), which allows us to define [DAGs](https://en.wikipedia.org/wiki/Directed_acyclic_graph). and automate the steps involved in data extraction/loading.


#### Installations 
- First install Docker. Instructions [here](https://docs.docker.com/get-docker/).
- Next install Docker Compose. Instructions [here](https://docs.docker.com/compose/install/.).

**NOTE:** This is a quickstart guide, hence shouldn't be used in production environments.

The `docker-compose.yaml` file used in this project is referenced (with few modifications) from the Airflow in Docker quick-start guide [here](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html). This file defines all the services neccessary to get the Airflow running (e.g: redis, scheduler, web server).

**modifications:**

- Official Airflow docker image under `x-airflow-common` in `docker-compose.yaml` is replaced (lines 48 to 50). I have referenced a external `Dockerfile` which pulls the airflow image, installs the google cloud sdk and python dependencies using pip. These are necessary to run the dags/scripts successfully.

- The lines from 62 to 67 in the current `docker-compose.yaml` are either added or modified. These help to setup the required environment varibales in the containers.

    ```yaml
    GOOGLE_APPLICATION_CREDENTIALS: /.google/credentials/google_credentials.json
    AIRFLOW_CONN_GOOGLE_CLOUD_DEFAULT: 'google-cloud-platform://?extra__google_cloud_platform__key_path=/.google/credentials/google_credentials.json'
    GCP_PROJECT_ID: '${GCP_PROJECT_ID}'
    GCP_GCS_BUCKET: '${GCP_GCS_BUCKET}'
    BIGQUERY_DATASET: '${BIGQUERY_DATASET}'
    ```
- Volumes with files required are added, so that they will be mounted (refer lines 68 to 76 in the docker-compose.yaml)

    ```yaml
    volumes:
    - ./dags:/opt/airflow/dags
    - ./logs:/opt/airflow/logs
    - ./plugins:/opt/airflow/plugins
    - ~/.config/gcloud/:/.config/gcloud:ro
    - ~/.google/credentials/:/.google/credentials:ro
    ```

#### Understanding the code

There are two dags defined, present in `dags/` folder and can also be seen in the airflow UI.

1. `reddit_etl.py` - This DAG exrtacts data for the last month and is scheduled to run on monthly basis. But you can also manually trigger it from UI to test run it.
2. `reddit_etl_historical.py` - This DAG exrtacts historical data and not scheduled to run. Trigger it manually to extract, save & load 2022 data into gcs, bigquery.

If you observe the `reddit_etl.py` code file, it imports the `run_etl` function from the `api_to_gcs.py` file - which has the python code to fetch the data from Pushshift API and save it to GCS. The pipeline is scheduled for a monthly cadence (ideally in the first week) and fetch the posts from a given sub-reddit for the previous month. Since `limit` is set to `None` in the `fetch_data` function, it should return all posts created in the previous month.

The DAG defined is pretty simple & does following three tasks
1. `api_to_gcs_task`: Extracts the Reddit data from API and the saves to the given gcs bucket in CSV format.
2. `delete_ext_table_task`: Deletes the external table definition or view if already exists.
3. `create_bq_table_task`: Creates a external table in the provided bigquery dataset.

![DAG](../static/reddit-etl-dag.png)

Similary, `reddit_etl_historical` takes `year` as input argument and extracts historical data for entire year.

#### Execution steps

- Make sure gcp credentials json exists at `~/.google/credentials/` directory, so it will be mounted. It should be named as google_credentials.json else the dags will fail!

- Make sure you are in `airflow` directory, else navigate to it using `cd` command. Then create folders required by airflow using below command. These folders will be mounted to the airflow container.

    ```shell
    mkdir -p ./logs ./plugins
    ```

- Set the evironment variables. Replace the values `<PROJECT_ID>`, `<GCS_BUCKET>`, `<BQ_DS>` & run the below cmd. This create a `.env` with required env variable details. (refer the `dev.env` sample file in this directory)

    ```shell
    echo -e "AIRFLOW_UID=50000\nGCP_PROJECT_ID=<PROJECT_ID>\nGCP_GCS_BUCKET=<GCS_BUCKET>\nBIGQUERY_DATASET=<BQ_DS>"> .env
    ```
    <!-- `export $(xargs < .env)` -->

- Run the below commands to start the airflow (runs in detached mode). If commands run succesfully, visiting http://localhost:8080 in a browser should open airflow UI. If nothing shows up, give it a few more minutes & try again. Password and username are both `airflow`. For understanding the UI, can refer official [docs](https://airflow.apache.org/docs/apache-airflow/stable/ui.html).


    ```shell
    echo "builiding the images...This might take a while to complete..."
    docker-compose build

    echo "Running airflow-init..."
    docker-compose up airflow-init

    echo "Starting up airflow in detached mode..."
    docker-compose up -d

    echo "Airflow started successfully, running in detached mode."
    ```

- run this command to see the logs `docker-compose logs --follow`

- To stop all container associated to airflow run `docker-compose down`

**Optional Steps**
- Once containers are up & running, we can view them in Docker Desktop, or list them from the command line with:
    ```bash
    docker ps
    ```
- Once containers are up & running, we can even connect into a docker container and navigate around the filesystem:
    ```bash
    docker exec -it <CONTAINER ID> bash
    ```
- for stopping & deleting all container (along with images and data downloaded), use the below commands
    ```bash
    docker-compose down --volumes --rmi all
    ```
- As the containers are running under airflow user, your local user will loose permission to the `dags/` directory & will not be able to edit them. you can run this command (from inside airflow directory) to get them back after shutting down the docker containers.
    `sudo chown <user>:<user> -R ../airflow`