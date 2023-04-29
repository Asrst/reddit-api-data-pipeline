from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators import bigquery

from datetime import datetime,timedelta
import pyarrow as pa
import os, sys
from api_to_gcs import run_etl


AIRFLOW_HOME = os.environ.get('AIRFLOW_HOME', '/opt/airflow')
GCP_PROJECT_ID = os.environ.get('GCP_PROJECT_ID')
GCP_GCS_BUCKET = os.environ.get('GCP_GCS_BUCKET')
BIGQUERY_DATASET = os.environ.get('BIGQUERY_DATASET')
SUBREDDIT = 'ipl'


"""
DAG to extract Reddit data, load into AWS S3, and copy to AWS Redshift
"""

# Run our DAG daily and ensures DAG run will kick off
# once Airflow is started, as it will try to "catch up"
schedule_interval = "@daily"
start_date = days_ago(1)

default_args = {"owner": "airflow", 
                "retries": 1}

with DAG(
    dag_id="reddit_etl",
    description="Reddit API Data Pipeline",
    schedule_interval=schedule_interval,
    default_args=default_args,
    start_date=start_date,
    catchup=True,
    max_active_runs=1,
    tags=["RedditEtl"]) as dag:

    # extract_data = BashOperator(
    #     task_id="extract",
    #     bash_command=f"python /opt/airflow/scripts/etl.py {output_name}",
    #     dag=dag,
    # )

    dt_now = datetime.now().strftime("%Y%m%d")
    OUTPUT_FILENAME = f'posts-{dt_now}.csv'
    api_to_gcs_task = PythonOperator(
        task_id='upload_to_gcs',
        python_callable = run_etl,
        op_kwargs = {
            'subreddit': SUBREDDIT, 
            'bucket_name' : GCP_GCS_BUCKET,
            'save_path' : f'{SUBREDDIT}/{OUTPUT_FILENAME}'
        }
    )
    api_to_gcs_task.doc_md = "Extract Reddit data and store as CSV in GCS"
    
    create_bq_table_task = bigquery.BigQueryCreateExternalTableOperator(
                                task_id = f'create_ext_bq_table',
                                table_resource = {
                                    'tableReference': {
                                    'projectId': GCP_PROJECT_ID,
                                    'datasetId': BIGQUERY_DATASET,
                                    'tableId': SUBREDDIT,
                                    },
                                    'externalDataConfiguration': {
                                        'sourceFormat': 'CSV',
                                        'autodetect': True,
                                        'sourceUris': [f'gs://{GCP_GCS_BUCKET}/{SUBREDDIT}/*.csv'],
                                    },
                                }
    )
    create_bq_table_task.doc_md = "Copy CSV from to GCS to Bigquery table"

api_to_gcs_task >> create_bq_table_task