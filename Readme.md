
## Reddit-API-data-pipeline

**prerequisites**: 
- GCP Account & Terraform (for cloud workflows)
- Make sure Docker is installed & Logged in to the Docker CLI using `docker login`
- Install Requirements using requirements.txt to test/run the code.
- Reddit API requires Auth (skip if using pushshift API), login & create an app [here](https://www.reddit.com/prefs/apps)


### steps for cloud workflow

1. Run terraform to create/update GCP infra (refer the folder`/terraform`).
2. To test the etl, run `/scripts/test_pushshift.py`.
3. Automate the etl scripts to run monthly using Airflow (refer `/airflow` for detailed steps).
4. Transform data using "dbt" & Create a data mart.
5. Connect Superset to bigquery &  use newly created data mart to visualise the data.