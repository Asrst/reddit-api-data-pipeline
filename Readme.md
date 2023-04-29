
## Reddit-API-data-pipeline

**prerequisites**: 
- GCP Account & Terraform (for cloud workflows)
- Make sure Docker is installed & Logged in to the Docker CLI using `docker login`
- Install Requirements using requirements.txt to test/run the code.


### steps for cloud workflow

1. Run terraform to create/update GCP infra (refer the folder`/terraform`).
2. To test the etl, run `/scripts/test_reddit_api.py` (requires auth, refer here).
3. Automate the workflow using Airflow (refer `/airflow` for detailed steps).
4. Clean/Transform data with "dbt" & create a data mart.
5. Connect Superset to bigquery &  use newly created data mart to visualise the data.