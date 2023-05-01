
## Reddit-API-data-pipeline

## Objective:
Create a batch data pipeline to ingest Reddit data from its API (for any chosen sub-reddit). The end goal is build a dashboard/report, providing insight into the user engagement metrics of the selected subreddits.


### Architecture/Flow:
<!-- ![Reddit Data Ingestion Pipeline (Batch)](./static/reddit-data-pipeline-flow.png "Reddit Data Ingestion Pipeline (Batch)") -->
<img src="./static/reddit-data-pipeline-flow.png" width=79% height=79%>


**pre-requisites**: 
- GCP Account & Terraform (Cloud Storage & Biq Query will be used).
- Make sure Docker is installed & Logged in to the Docker CLI using `docker login`.
- Install Requirements using `requirements.txt` to test/run the code.
- Reddit API requires Auth, login & create an [app](https://www.reddit.com/prefs/apps) to get credentials (skip if using pushshift API).
- Singup for a free dbt cloud developer account & connect with github to read/write to this git repo.


### Steps/Instructions:

1. Run terraform to create/update GCP infra. Refer the folder ![`terraform`](./terraform/).
2. To extract and store the data to GCS, run `python3 /scripts/test_pushshift.py`.
3. To create big query external tables, run `python3 /scripts/test_bq_load.py`.
4. Automate the steps 2 & 3 to run monthly using Airflow. Refer ![`airflow`](./airflow/) for detailed steps.
4. Transform data using dbt & Create a data mart. Refer ![`dbt`](./dbt/) for detailed steps.
5. Connect Superset to bigquery &  use newly created data mart to visualise/report.


### Result/Output:
<img src="./static/superset-preset-reddit-analytics.jpg" width=79% height=79%>

**Important Note:** 
- preset.io (or superset) doesnt allow public dashboard sharing outside of workspace (users needs to be in same workspace for sharing to work). hence this dashboard will be unavailble publicly.
