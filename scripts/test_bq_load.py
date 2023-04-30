from google.cloud import bigquery, storage

SCHEMA_LIST = []

def load_from_gcs_to_bq(dataset, table_name, gcs_uri):

    """
    create big query table
    """
    
    bq_client = bigquery.Client()
    bq_dataset = bq_client.dataset(dataset)
    bq_table = bq_dataset.table(table_name)

    job_config = bigquery.LoadJobConfig(autodetect=True)
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.field_delimiter = ','
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
    job_config.null_marker = ''
    # job_config.schema = SCHEMA_LIST
    job_config.allow_quoted_newlines = True

    load_job = bq_client.load_table_from_uri(gcs_uri, bq_table, 
                                             job_config=job_config
                                             )
    # wait till complete
    load_job.result() 

    # print("state of job is: " + load_job.state)
    # print("errors: " + load_job.errors)

    table_out = bq_client.get_table(bq_table)
    print(f"# of rows in table @ {table_name}: {table_out.num_rows}")


def load_from_gcs_to_bq_ext(dataset, table_name, gcs_uri):

    bq_client = bigquery.Client()
    bq_table = bq_client.dataset(dataset).table(table_name)

    # Configure the external data source.
    external_config = bigquery.ExternalConfig("CSV")
    external_config.source_uris = [gcs_uri]
    external_config.autodetect = True

    ext_csv_opts = bigquery.CSVOptions()
    ext_csv_opts.allow_quoted_newlines = True
    external_config.csv_options = ext_csv_opts

    # Configure partitioning options.
    # hive_partitioning_opts = bigquery.HivePartitioningOptions()
    # We have a "/dt=YYYY-MM-DD/" path component in our example files as documented above.
    # Autolayout will expose this as a column named "dt" of type DATE.
    # hive_partitioning_opts.mode = "AUTO"
    # hive_partitioning_opts.require_partition_filter = True
    # hive_partitioning_opts.source_uri_prefix = source_uri_prefix
    # external_config.hive_partitioning = hive_partitioning_opts

    table = bigquery.Table(bq_table)
    table.external_data_configuration = external_config

    # only creates new external table, error's if table already exists.
    table = bq_client.create_table(table) # exists_ok=True, won't update existing table.
    print("Created External Table: {}.{}".format(table.dataset_id, table.table_id))



if __name__ == "__main__":
    bq_dataset = "reddit_api"
    table_name = "ext_ipl"
    gcs_uri = f'gs://dl-reddit-api-404/ipl/posts-2022-*.csv'
    load_from_gcs_to_bq_ext(bq_dataset, table_name, gcs_uri)

